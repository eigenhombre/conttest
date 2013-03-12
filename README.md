# conttest

Continuous testing helper, adapted from [1], but which makes no
assumption about what tests you might want to run continuously while
developing.  For more information, see [this blog post](http://eigenhombre.com/testing/2012/03/31/ontinuous-testing-in-python-clojure-and-blub/).

**Any command supplied to the script will be run once and
then repeated any time the code in the current working directory
changes.**  You may wish to edit the IGNORE_* tuples to suit your
particular setup.

Note that ANY command you supply the script will be run, so be
careful.  You have been warned!

[1] Adapted from https://github.com/brunobord/tdaemon/blob/master/tdaemon.py

### Installation

    ./setup.py install  # from source
or

    easy_install conttest  # or use pip instead of easy_install

### Usage examples

    conttest nosetests
    conttest 'nosetests -q && pep8 -r .'

Placing a file .conttest-excludes in the current working directory
will exclude subdirectories, e.g.:

    .svn
    .git
    build
    install

will skip checking for changes in those directories.  This can save
quite a bit of time and CPU during normal operation.  Currently this
works for top-level directories only!

## Author

[John Jacobsen](http://eigenhombre.com)

## License

Eclipse Public License

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF THIRD PARTY RIGHTS. IN
NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
