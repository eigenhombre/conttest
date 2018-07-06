# conttest

<a href="https://travis-ci.org/eigenhombre/continuous-testing-helper"><img src="https://travis-ci.org/eigenhombre/continuous-testing-helper.svg?branch=master"></a>

Continuous testing helper, adapted from [1], but which makes no
assumption about what tests you might want to run continuously while
developing.  For more information, see
[this blog post](http://zerolib.com/continuous-testing.html).

**Any command supplied to the script will be run once and then
repeated any time a file in the current working directory changes,**
except for files excluded using `.conttest-excludes` as described below.

Note that ANY command you supply the script will be run, so be
careful.  You have been warned!

[1] https://github.com/brunobord/tdaemon/blob/master/tdaemon.py

### Installation

    ./setup.py install  # from source
or

    pip install conttest  # use sudo if installing globally

### Usage examples

    conttest nosetests
    conttest 'nosetests -q && pep8 -r .'

Placing a file `.conttest-excludes` in the current working directory
will exclude subdirectories, e.g.:

    .svn$
    .git
    build
    vendor/elastic*
    install

will match files against the listed regular expressions and skip checking
for changes in those directories.  This can save quite a bit of time and CPU
during normal operation.

## Author

[John Jacobsen](http://zerolib.com)

## License

Eclipse Public License

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF THIRD PARTY RIGHTS. IN
NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
