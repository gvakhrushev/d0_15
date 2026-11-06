"""Pinned-source transient failures are not missing source evidence."""
import os
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock
from tools import proof_architecture as proof


class PinTransientTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = pathlib.Path(temp.name)
        subprocess.run(['git','init','-q'], cwd=self.root, check=True)
        subprocess.run(['git','config','user.name','Fixture'],cwd=self.root,check=True)
        subprocess.run(['git','config','user.email','fixture@example.invalid'],cwd=self.root,check=True)
        (self.root/'present.md').write_bytes(b'precise source\n')
        (self.root/'large.md').write_bytes(b'x' * 4_000_001)
        (self.root/'nested').mkdir()
        (self.root/'nested'/'inside.md').write_bytes(b'nested source\n')
        subprocess.run(['git','add','.'],cwd=self.root,check=True)
        subprocess.run(['git','commit','-qm','pin'],cwd=self.root,check=True)
        self.commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=self.root,text=True).strip()
        self.blob=subprocess.check_output(['git','rev-parse','HEAD:present.md'],cwd=self.root,text=True).strip()
        self.ref={'commit':self.commit,'path':'present.md','blob':self.blob}

    def test_success_missing_mismatch_and_too_large_are_distinct(self):
        self.assertEqual(proof._read_pinned_source(self.root,dict(self.ref),{}),('pinned_snapshot',b'precise source\n'))
        self.assertEqual(proof._read_pinned_source(self.root,{**self.ref,'path':'absent.md'},{}),('external_reference_only',None))
        self.assertEqual(proof._read_pinned_source(self.root,{**self.ref,'blob':'0'*40},{}),('pin_mismatch',None))
        status,_=proof._read_pinned_source(self.root,{**self.ref,'path':'large.md','blob':None},{})
        self.assertEqual(status,'pinned_source_too_large')

    def test_timeout_or_launch_failure_is_diagnostic_not_missing_or_cached(self):
        for exc in (subprocess.TimeoutExpired(['git'],5), FileNotFoundError('git unavailable')):
            cache={}; ref=dict(self.ref)
            with self.subTest(exc=type(exc).__name__), mock.patch.object(proof.subprocess,'run',side_effect=exc):
                with self.assertRaisesRegex(proof.PinnedSourceTransientError,'pinned source Git'):
                    proof._read_pinned_source(self.root,ref,cache)
            self.assertEqual(cache,{})
            self.assertEqual(ref,self.ref)

    def test_git_nonzero_and_malformed_batch_do_not_claim_missing(self):
        for ret in (subprocess.CompletedProcess([],128,b'',b'operational failure'),
                    subprocess.CompletedProcess([],0,b'unexpected\n',b'')):
            cache={}
            with self.subTest(returncode=ret.returncode),mock.patch.object(proof.subprocess,'run',return_value=ret):
                with self.assertRaises(proof.PinnedSourceTransientError):
                    proof._read_pinned_source(self.root,dict(self.ref),cache)
            self.assertEqual(cache,{})

    def test_blob_read_timeout_does_not_mutate_implicit_pin(self):
        real=proof.subprocess.run; ref={**self.ref,'blob':None};cache={}
        def run(args,*a,**kw):
            if args[:3]==['git','cat-file','blob']:
                raise subprocess.TimeoutExpired(args,5)
            return real(args,*a,**kw)
        with mock.patch.object(proof.subprocess,'run',side_effect=run):
            with self.assertRaises(proof.PinnedSourceTransientError):
                proof._read_pinned_source(self.root,ref,cache)
        self.assertIsNone(ref['blob']);self.assertEqual(cache,{})

    def test_missing_tree_object_is_not_external_reference(self):
        tree = subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=self.root,text=True).strip()
        object_path=self.root/'.git'/'objects'/tree[:2]/tree[2:]
        self.assertTrue(object_path.is_file())
        object_path.chmod(0o600)
        object_path.unlink()
        for name in ('present.md','absent.md'):
            with self.subTest(name=name):
                with self.assertRaisesRegex(proof.PinnedSourceTransientError, 'tree lookup'):
                    proof._read_pinned_source(self.root,{**self.ref,'path':name}, {})

    def test_corrupt_commit_is_not_absence(self):
        obj=self.root/'.git'/'objects'/self.commit[:2]/self.commit[2:]
        obj.chmod(0o600); obj.write_bytes(b'not a zlib stream')
        cache={};ref=dict(self.ref)
        with self.assertRaisesRegex(proof.PinnedSourceTransientError,'commit lookup'):
            proof._read_pinned_source(self.root,ref,cache)
        self.assertEqual(cache,{});self.assertEqual(ref,self.ref)

    def test_missing_blob_object_is_failure_not_mismatch(self):
        object_path=self.root/'.git'/'objects'/self.blob[:2]/self.blob[2:]
        self.assertTrue(object_path.is_file())
        object_path.chmod(0o600)
        object_path.unlink()
        with self.assertRaisesRegex(proof.PinnedSourceTransientError, 'blob size'):
            proof._read_pinned_source(self.root,dict(self.ref), {})

    def test_partial_clone_missing_blob_does_not_lazy_fetch(self):
        for name,value in (('remote.origin.url','file:///nonexistent/promisor.git'),
                           ('remote.origin.promisor','true'),('extensions.partialClone','origin')):
            subprocess.run(['git','config',name,value],cwd=self.root,check=True)
        obj=self.root/'.git'/'objects'/self.blob[:2]/self.blob[2:]
        obj.chmod(0o600); obj.unlink()
        real=proof.subprocess.run; traces=[]
        def run(args,*a,**kw):
            self.assertEqual(kw['env'].get('GIT_NO_LAZY_FETCH'),'1')
            result=real(args,*a,**kw); traces.append(result.stderr)
            return result
        with mock.patch.dict(os.environ,{'GIT_TRACE':'1'}),mock.patch.object(proof.subprocess,'run',side_effect=run):
            with self.assertRaisesRegex(proof.PinnedSourceTransientError,'blob size'):
                proof._read_pinned_source(self.root,dict(self.ref),{})
        self.assertNotIn(b'git fetch',b'\n'.join(traces))

    def test_inherited_git_redirects_do_not_select_foreign_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            foreign=pathlib.Path(tmp)
            subprocess.run(['git','init','-q'],cwd=foreign,check=True)
            subprocess.run(['git','config','user.name','Foreign'],cwd=foreign,check=True)
            subprocess.run(['git','config','user.email','foreign@example.invalid'],cwd=foreign,check=True)
            (foreign/'foreign.md').write_bytes(b'foreign source\n')
            subprocess.run(['git','add','.'],cwd=foreign,check=True)
            subprocess.run(['git','commit','-qm','foreign'],cwd=foreign,check=True)
            commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=foreign,text=True).strip()
            ref={'commit':commit,'path':'foreign.md','blob':None}
            for variable,value in (('GIT_DIR',foreign/'.git'),('GIT_OBJECT_DIRECTORY',foreign/'.git'/'objects')):
                with self.subTest(variable=variable),mock.patch.dict(os.environ,{variable:str(value)}):
                    self.assertEqual(proof._read_pinned_source(self.root,dict(ref),{}),('external_reference_only',None))

    def test_missing_intermediate_tree_is_not_external_reference(self):
        tree=subprocess.check_output(['git','rev-parse','HEAD:nested'],cwd=self.root,text=True).strip()
        obj=self.root/'.git'/'objects'/tree[:2]/tree[2:]
        obj.chmod(0o600); obj.unlink()
        for name in ('nested/inside.md', 'nested/absent.md'):
            with self.subTest(name=name):
                with self.assertRaisesRegex(proof.PinnedSourceTransientError, 'tree lookup'):
                    proof._read_pinned_source(self.root,{**self.ref,'path':name}, {})

    def test_success_implicit_pin_binds_only_after_verified_bytes(self):
        ref={**self.ref,'blob':None}; cache={}
        self.assertEqual(proof._read_pinned_source(self.root,ref,cache),('pinned_snapshot',b'precise source\n'))
        self.assertEqual(ref['blob'],self.blob); self.assertIs(ref['pin_complete'],True)

    def test_control_char_citation_is_not_sent_to_git(self):
        with mock.patch.object(proof.subprocess,'run',side_effect=AssertionError('Git called')):
            self.assertEqual(proof._read_pinned_source(self.root,{**self.ref,'path':'bad\n.md'},{}),('citation_only',None))

if __name__=='__main__': unittest.main()
