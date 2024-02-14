from nuclear import shell

from tests.utils import StdoutCap, assert_multiline_match


def test_match_files_from_stdin():
    with StdoutCap() as cap:
        # find -name '_*.mp3'
        shell("printf './res/2mp3/_1.mp3\n./res/2mp3/_2.mp3' | regex-rename '_(.*).mp3'", print_stdout=True)
        assert cap.uncolor(), 'captured stdout should not be empty'
    assert_multiline_match(cap.uncolor(), r'''
\[.*\] DEBUG matching regular expression pattern to files: pattern=_\(\.\*\).mp3 replacement=None dry_run=True full_match=False recursive=False padding=None
\[.*\] DEBUG reading input files from stdin
\[.*\] INFO  matched file: file=res/2mp3/_1.mp3 group_1=1
\[.*\] INFO  matched file: file=res/2mp3/_2.mp3 group_1=2
\[.*\] INFO  files matched the pattern: matched=2 mismatched=0
'''.strip())
