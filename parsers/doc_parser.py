import subprocess
import os
import errno


class Parser():
    """Extract text from doc files using antiword.
    """
    """The :class:`.ShellParser` extends the :class:`.BaseParser` to make
    it easy to run external programs from the command line with
    `Fabric <http://www.fabfile.org/>`_-like behavior.
    """

    def run(self, args):
        """Run ``command`` and return the subsequent ``stdout`` and ``stderr``
        as a tuple. If the command is not successful, this raises a
        :exc:`textract.exceptions.ShellError`.
        """

        # run a subprocess and put the stdout and stderr on the pipe object
        try:
            pipe = subprocess.Popen(
                args,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
        except OSError as e:
            if e.errno == errno.ENOENT:
                # File not found.
                # This is equivalent to getting exitcode 127 from sh
                raise exceptions.ShellError(
                    ' '.join(args), 127, '', '',
                )

        # pipe.wait() ends up hanging on large files. using
        # pipe.communicate appears to avoid this issue
        stdout, stderr = pipe.communicate()

        # if pipe is busted, raise an error (unlike Fabric)
        if pipe.returncode != 0:
            raise exceptions.ShellError(
                ' '.join(args), pipe.returncode, stdout, stderr,
            )

        return stdout, stderr


    def extract(self, filename, **kwargs):
        stdout, stderr = self.run(['antiword', filename])
        return stdout