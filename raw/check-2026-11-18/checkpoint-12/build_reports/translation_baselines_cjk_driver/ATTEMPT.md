# Interrupted diagnostic driver attempt

This attempt was stopped during the first Korean pass after the initial wrapper retained an xparse dispatcher whose implementation was then replaced, causing recursive dispatch. The helper was corrected to copy document commands with `NewCommandCopy`; a new immutable stage is used for the retry. No source file was changed, no PDF was produced, and no later source behavior was assessed by this attempt.
