import Lake
open Lake DSL

package d0_lean_formalization where
  -- Lake dependency sources and build artifacts are kept outside the repository
  -- by default (Lake uses its own cache location, typically under ~/.lake or
  -- a user-configured LAKE_HOME). This keeps the repo itself small and portable.
  -- The committed lean-toolchain + lake-manifest.json + lean sources are sufficient
  -- for reproducibility.
  --
  -- If you want a custom shared external cache directory, set it via environment
  -- variables or uncomment and edit the lines below (local only, do not commit):
  -- packagesDir := "../.lake-d0/packages"
  -- buildDir := "../.lake-d0/build"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

lean_lib D0 where
