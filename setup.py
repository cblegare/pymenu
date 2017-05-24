#!/usr/bin/python3.5
# coding: utf8


"""This scripts lays building blocks for development tooling."""


from distutils.version import LooseVersion
from functools import reduce
import email.utils
import errno
import fnmatch
import os
import platform
import setuptools
import shutil
try:
    # python 3
    from urllib.parse import urlparse
except ImportError:
    # python 2
    from urlparse import urlparse
import six


__all__ = (
    'ProjectMetadata',
    'Clean',

    'Documentation',
)


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

PYTHON_VERSION = platform.python_version_tuple()

DEFAULT_VERSION = '0.1.0'


class ProjectMetadata(object):
    """
    This hold distribution information primarily used at build time.

    Properties of this class are intended to roughly fit the
    `metadata
    <https://docs.python.org/2/distutils/setupscript.html#additional-meta-data>`_
    expected by keyword arguments by the :func:`setuptools.setup` function.

    Since we use *setuptools*, you may wish to read about
    `new and changed setup keywords
    <http://setuptools.readthedocs.io/en/latest/setuptools.html?highlight=keywords#new-and-changed-setup-keywords>`.
    """

    def __init__(self):
        """Initialize some cached or internal storage of data."""
        self._version = None

    @property
    def name(self):
        """
        Name of the package.

        Note:
            This field is required by :func:`setuptools.setup`

        Returns:
             str: A short string
        """
        value = 'pymenu'
        return self._ensure_short_string(value)

    @property
    def description(self):
        """
        Short, summary description of the package.

        Returns:
             str: A short string
        """
        value = 'A general purpose menu API.'
        return self._ensure_short_string(value)

    @property
    def version(self):
        """
        Version of this release.

        Note:
            This field is required by :func:`setuptools.setup`

        Returns:
             str: A short string
        """
        if self._version is None:
            try:
                self._version = str(LooseVersion(read_file('VERSION')))
            except (OSError, IOError):
                self._version = str(LooseVersion(os.getenv('_VERSION',
                                                           DEFAULT_VERSION)))

        return self._ensure_short_string(self._version)

    @property
    def url(self):
        """
        Home page for the package.

        Note:
            This field is required by :func:`setuptools.setup`

        Returns:
             str: A URL
        """
        value = 'https://github.com/cblegare/pymenu'
        return self._ensure_url(value)

    @property
    def download_url(self):
        """
        Location where the package may be downloaded.

        Returns:
             str: A URL
        """
        value = '{!s}/tarball/{!s}'.format(self.url, self.version)
        return self._ensure_url(value)

    @property
    def license(self):
        """
        License for the package.

        Note:
            The "license" field is a text indicating the license
            covering the package where the license is not a selection
            from the "License" Trove classifiers. See the :attr:`~classifiers`
            field. Notice that there's a "licence" distribution option
            which is deprecated but still acts as an alias for license.

        Returns:
             str: A short string
        """
        value = 'GNU Lesser General Public License v3'
        return self._ensure_short_string(value)

    @property
    def keywords(self):
        """
        A whitespace-separated list of keywords about this project.

        I have been able to find documentation about this parameter but it
        is clearly used in the setuptools documentation in the example
        provided for `basic usage
        <http://setuptools.readthedocs.io/en/latest/setuptools.html?highlight=keywords#basic-use>`
        """
        return ''

    @property
    def author(self):
        """
        Package author’s name.

        Either the author or the maintainer must be identified. If
        maintainer is provided, distutils lists it as the author in
        PKG-INFO.

        Returns:
             str: A short string
        """
        value = 'Charles Bouchard-Légaré'
        return self._ensure_short_string(value)

    @property
    def author_email(self):
        """
        Email address of the package author.

        See also :attr:`~author`

        Returns:
             str: An email address
        """
        value = 'cblegare.atl@ntis.ca'
        return self._ensure_email_address(value)

    @property
    def classifiers(self):
        """
        A list of classifiers.

        Feel free to consult
        `all possibles classifiers
        <https://pypi.python.org/pypi?%3Aaction=list_classifiers>`.

        Returns:
             List[str]: A list of short strings
        """
        value = ['Development Status :: 2 - Pre-Alpha',
                 'Environment :: Console',
                 'Environment :: X11 Applications',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: '
                 'GNU Lesser General Public License v3 or later (LGPLv3+)',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Topic:: Desktop Environment',
                 'Topic :: Utilities']
        return [self._ensure_short_string(string) for string in value]

    @property
    def packages(self):
        """
        A list of packages to distribute (and all their submodules).

        It's usage is explained in
        `distutils documentation
        <https://docs.python.org/2/distutils/setupscript.html#listing-whole-packages>`

        You may also read about :func:`setuptools.find_packages` function and
        `it's usage
        <http://setuptools.readthedocs.io/en/latest/setuptools.html?highlight=keywords#using-find-packages>`.

        Returns:
             List[str]: A list of strings
        """
        if PYTHON_VERSION < ('3', '3'):
            find_packages = setuptools.find_packages
        else:
            find_packages = setuptools.PEP420PackageFinder.find
        value = find_packages(str(PROJECT_ROOT), exclude=['docs*',
                                                          'test*',
                                                          'requirements'])
        return [self._ensure_short_string(package) for package in value]

    @property
    def install_requires(self):
        """
        Production dependancies.

        A string or list of strings specifying what other distributions need
        to be installed when this one is.

        It's usage is explained in `setuptools documentation
        <http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-dependencies>`

        Returns:
             List[str]: A list of short strings
        """
        return ['pyxdg', 'anytree']

    @property
    def tests_require(self):
        """
        Automated tests dependancies.

        If your project’s tests need one or more additional packages besides
        those needed to install it, you can use this option to specify them.

        It's usage is explained in `setuptools documentation
        <http://setuptools.readthedocs.io/en/latest/setuptools.html#new-and-changed-setup-keywords>`

        Returns:
             List[str]: A list of short strings
        """
        return ['coverage',
                'pytest-cov',
                'pytest-flake8',
                'pytest',
                'xenon',
                'flake8',
                'flake8-quotes>=0.3',
                'pycodestyle>=2.2']

    @property
    def setup_requires(self):
        """
        A string or list of strings specifying what other distributions need to
        be present in order for the setup script to run. setuptools will
        attempt to obtain these (even going so far as to download them using
        EasyInstall) before processing the rest of the setup script or
        commands. This argument is needed if you are using distutils extensions
        as part of your build process; for example, extensions that process
        `setup()` arguments and turn them into EGG-INFO metadata files.

        Note:
            Projects listed in setup_requires will NOT be automatically
            installed on the system where the setup script is being run. They
            are simply downloaded to the ./.eggs directory if they’re not
            locally available already. If you want them to be installed, as
            well as being available when the setup script is run, you should
            add them to install_requires and setup_requires.

        Returns:
             List[str]: A list of short strings
        """
        return []

    @property
    def extras_require(self):
        """
        A dictionary mapping names of `extras` (optional features of your
        project) to strings or lists of strings specifying what other
        distributions must be installed to support those features.

        See Also:
            http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies

        Returns:
            Dict: Lists of dependencies indexed by the feature they enable.
        """
        XDG = ['pyxdg']
        develop = ['sphinx>=1.5',
                   'sphinx_rtd_theme']
        return {'XDG': XDG,
                'develop': develop,
                'all': XDG + develop}

    def setup(self):
        """Run :func:`setuptools.setup` using :func:~`raw`."""
        return setuptools.setup(**self.raw())

    def raw(self):
        """
        Create a generic dict representation.

        Provides a uniform access to all distribution data as python
        primitives, exactly the same one would provide to
        :func:`setuptools.setup`

        Returns:
            dict: Keyword arguments for :func:`setuptools.setup`.
        """
        return dict(name=self.name,
                    version=self.version,
                    description=self.description,
                    url=self.url,
                    license=self.license,
                    author=self.author,
                    author_email=self.author_email,
                    classifiers=self.classifiers,
                    packages=self.packages,
                    include_package_data=True,
                    entry_points={
                        'console_scripts': [
                            '{module!s}={module!s}.cli:main'.format(
                                module=self.name)
                        ]
                    },
                    cmdclass={'docs': Documentation,
                              'clean': Clean,
                              'mk_req': Requirements},
                    install_requires=self.install_requires,
                    tests_require=self.tests_require,
                    setup_requires=self.setup_requires,
                    extras_require=self.extras_require)

    def __str__(self):
        """Provide a human-readable representation."""
        import pprint
        return pprint.pformat(self.raw(),)

    @staticmethod
    def _ensure_short_string(string):
        string = six.u(string)
        assert len(string) <= 200
        return string

    @staticmethod
    def _ensure_long_string(string):
        string = six.u(string)
        return string

    @staticmethod
    def _ensure_email_address(string):
        string = six.u(string)
        _, email_str = email.utils.parseaddr(str(string))
        assert email_str == str(string)
        return string

    @staticmethod
    def _ensure_url(string, qualifying=None):
        string = six.u(string)
        min_attributes = ('scheme', 'netloc')

        qualifying = min_attributes if qualifying is None else qualifying
        token = urlparse(str(string))
        valid = all([getattr(token, qualifying_attr)
                     for qualifying_attr in qualifying])
        assert valid
        return string


class Clean(setuptools.Command):
    """Custom clean command to tidy up the project."""

    description = 'Custom clean command to tidy up the project.'
    user_options = []
    default_patterns = ['build',  'dist', '*.egg-info', '*.egg', '*.pyc',
                        '*.pyo', '*~', '__pycache__', '.tox', '.coverage',
                        'htmlcov']

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        for pattern in self.default_patterns:
            self._remove_matching_files(pattern)

    def _remove_matching_files(self, pattern):
        for path in find_files(pattern):
            self.announce('Cleaning path {!s}'.format(path), 2)
            shutil.rmtree(path, ignore_errors=True)


class Requirements(setuptools.Command):
    """Write requirements file."""

    description = 'Write requirements file.'
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        metadata = ProjectMetadata()

        dependencies = []
        dependencies.extend(metadata.setup_requires)
        dependencies.extend(metadata.install_requires)
        dependencies.extend(metadata.tests_require)

        requirements_filepath = os.path.join(PROJECT_ROOT, 'requirements.txt')

        with open(requirements_filepath, 'w') as opened:
            opened.write('\n'.join(set(dependencies)))


class Documentation(setuptools.Command):
    """
    Make the documentation (without the *Make* program).

    .. note::

        This command will not allow any warning from `Sphinx`_, treating
        them as errors.

    .. _Sphinx: http://www.sphinx-doc.org/
    """

    description = 'create documentation distribution'
    user_options = [
        ('builder=', None, 'documentation output format '
                           '[default: html]'),
        ('dist-dir=', None, 'directory to put final built distributions in '
                            '[default: dist/docs]'),
        ('build-dir=', None, 'temporary directory for creating the '
                             'distribution '
                             '[default: build/docs]'),
        ('src-dir=', None, 'documentation source directory '
                           '[default: docs]'),
        ('ignore-warnings', None, 'let the documentation be built even if '
                                  'there are warnings [default: False]')
    ]

    targets = {
        'html': {
            'comment': 'The HTML pages are in {build_dir!s}.',
        },
        'dirhtml': {
            'comment': 'The HTML pages are in {build_dir!s}.',
        },
        'singlehtml': {
            'comment': 'The HTML pages are in {build_dir!s}.',
        },
        'latex': {
            'comment': 'The LaTeX files are in {build_dir!s}.',
        },
    }

    def initialize_options(self):
        """Set default values for options."""
        import os
        # Each user option must be listed here with their default value.
        project_directory = PROJECT_ROOT

        self.builder = 'html'
        self.dist_dir = os.path.join(PROJECT_ROOT, 'dist', 'docs')
        self.build_dir = os.path.join(PROJECT_ROOT, 'build', 'docs')
        self.src_dir = os.path.join(PROJECT_ROOT, 'docs')
        self.ignore_warnings = False

    def finalize_options(self):
        """Post-process options."""
        self.ignore_warnings = bool(self.ignore_warnings)
        if self.builder in self.targets:
            self._actual_targets = [self.builder]
        elif self.builder == 'all':
            self._actual_targets = self.targets.keys()
        else:
            self._actual_targets = []

        # package_dir may be None, in that case use the current directory.
        metadata = self.distribution.metadata
        self.code_dir =  os.path.abspath((self.distribution.package_dir
                                          or {'': metadata.name})[''])
        self._canonical_directories()

        self.announce(
            'Building {!s} documentation'.format(self.builder), 2)
        self.announce(
            '  using source at "{!s}"'.format(self.src_dir), 2)
        self.announce(
            '  putting work files at "{!s}"'.format(self.build_dir), 2)
        self.announce(
            '  distributing documentation at "{!s}"'.format(self.dist_root), 2)
        self.announce(
            '  looking for code at "{!s}"'.format(self.code_dir), 2)

    def run(self):
        """Run command."""
        result_dirs = {}
        for target in self._actual_targets:
            result_dirs[target] = self._build_doc(target)
        for target, result_dir in result_dirs.items():
            self.announce('Documentation target "{!s}" : {!s}'.format(
                target,
                self.targets[target]['comment'].format(
                    build_dir=result_dir)), 2)

    def _canonical_directories(self):
        self.dist_root = os.path.abspath(mkdir_p(self.dist_dir))
        self.build_dir = os.path.abspath(mkdir_p(self.build_dir))
        self.src_dir = os.path.abspath(mkdir_p(self.src_dir))

    def _build_source(self):
        import sphinx.apidoc
        build_dir = self.src_dir

        # metadata contains information supplied in setup()
        metadata = self.distribution.metadata

        sphinx_apidoc_opts = [
            '',
            '--module-first',   # Put module documentation before submodule
                                # documentation
            '--doc-project', metadata.name,
            '--output-dir', build_dir,
            '--maxdepth', 4,
            '--module-first',
            PROJECT_ROOT,  # All the project is sourced
            'setup.py',
        ]

        excluded_subdirectories = [directory
                          for directory in os.listdir(PROJECT_ROOT)
                          if os.path.isdir(directory)
                                   and directory not in [metadata.name,
                                                         'tests']]

        sphinx_apidoc_opts.extend(excluded_subdirectories)

        canonical_opts = [str(arg) for arg in sphinx_apidoc_opts]

        self.announce('  Invoking sphinx : '
                      '"{!s}"'.format(' '.join(canonical_opts)))
        sphinx.apidoc.main([str(arg) for arg in sphinx_apidoc_opts])

        return build_dir

    def _build_doc(self, target):
        import shutil
        import sphinx

        rst_src = self._build_source()
        metadata = self.distribution.metadata

        build_dir = os.path.join(self.build_dir, target)
        dist_dir = os.path.join(self.dist_root, target)

        cached_directory = os.path.join(os.path.dirname(build_dir), 'doctrees')

        all_sphinx_opts = [
            '',
            '-b', target,            # builder to use; default is html
            '-d', cached_directory,  # path for the cached doctree files
            '-n',                    # warn about all missing references
            '-q',                    # no output on stdout, warnings on stderr
            '-T',                    # show full traceback on exception
            '-D', 'project={!s}'.format(metadata.name),
            '-D', 'version={!s}'.format(metadata.version)
        ]

        if not self.ignore_warnings:
            all_sphinx_opts.append('-W')

        all_sphinx_opts.append(rst_src)
        all_sphinx_opts.append(build_dir)

        sphinx.build_main([str(arg) for arg in all_sphinx_opts])
        shutil.rmtree(str(dist_dir), ignore_errors=True)
        mkdir_p(os.path.dirname(dist_dir))
        shutil.copytree(str(build_dir), str(dist_dir))

        return dist_dir


def compose(*functions):
    """
    Compose provided functions.

    Here is an example usage::

        >>>def f(x):
        ...    return x+1
        ...
        >>> def g(y):
        ...    return y**2
        ...
        >>> f_o_g = compose(f, g)
        >>> f_o_g(1) == f(g(1))
        True
        >>> f_o_g(1)
        2
        >>> g_o_f =  compose(g, f)
        >>> g_o_f(1) == g(f(1))
        True
        >>> g_o_f(1)
        4
    """
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def read_file(file_path):
    """Read text from file relative to the project root."""
    return open(os.path.join(PROJECT_ROOT, str(file_path))).read()


def list_from_file(file_path):
    content = read_file(file_path)
    return [line.strip() for line in content.splitlines() if line]


def find_files(directory, pattern):
    """Generate file names matching pattern recursively found in directory."""
    for root, dirs, files in os.walk(str(directory)):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


def mkdir_p(path):
    """
    Behave like ``mkdir -b``

    Args:
        path (str):

    Returns:
        str: resulting path
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    return path


def main():
    """Main entry point."""
    meta = ProjectMetadata()
    meta.setup()


if __name__ == '__main__':
    main()
