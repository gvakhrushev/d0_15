import D0.Foundation.VerificationTransferApplication

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.TheoryTransfer
open D0.Foundation.VerificationTransferApplication

#check FutureExecution.profile_step_congr
#check FutureExecution.quotientStep
#check FutureExecution.profile_run
#check NativeContextCoverage.native_profile_eq_iff
#check hiddenBit_same_current
#check hiddenBit_different_future
#check visible_only_memory_cannot_decode_hiddenBit_futures
#check visibleBit_same_all_source_futures
#check extraBit_different_native_futures
#check extra_native_test_prevents_coverage
#print axioms FutureExecution.profile_step_congr
#print axioms FutureExecution.quotientStep
#print axioms FutureExecution.profile_run
#print axioms NativeContextCoverage.native_profile_eq_iff
#print axioms hiddenBit_same_current
#print axioms hiddenBit_different_future
#print axioms visible_only_memory_cannot_decode_hiddenBit_futures
#print axioms extra_native_test_prevents_coverage

-- The conclusion is restricted to words and tests of F.
example (F : FutureExecution) (s t : F.State)
    (h : F.profile s = F.profile t) (w : List F.Action) (q : F.Test) :
    F.observe (F.run w s) q = F.observe (F.run w t) q := by
  exact congrFun (congrFun h w) q
