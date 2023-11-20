#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	JOSE implementation in Python
Summary(pl.UTF-8):	Implementacja JOSE w Pythonie
Name:		python-jose
# keep 3.2.x here for python2 support
Version:	3.2.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/python-jose/
Source0:	https://files.pythonhosted.org/packages/source/p/python-jose/python-jose-%{version}.tar.gz
# Source0-md5:	382a4da9ec39a3fb872fd1cf672b8a57
Patch0:		%{name}-requirements.patch
URL:		https://pypi.org/project/python-jose/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-pytest-runner
BuildRequires:	python-setuptools >= 1:39.2.0
%if %{with tests}
BuildRequires:	python-cryptography
BuildRequires:	python-ecdsa
BuildRequires:	python-pytest
BuildRequires:	python-pytest-cov
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-pytest-runner
BuildRequires:	python3-setuptools >= 1:39.2.0
%if %{with tests}
BuildRequires:	python3-cryptography
BuildRequires:	python3-ecdsa
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-six
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
# for Sphinx 1.2
#BuildRequires:	python-sphinxcontrib-napoleon >= 0.3.4
BuildRequires:	sphinx-pdg-2 >= 1.3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JOSE is a framework intended to provide a method to securely transfer
claims (such as authorization information) between parties. The JOSE
framework provides a collection of specifications to serve this
purpose.

%description -l pl.UTF-8
JOSE to szkielet mający na celu zapewnienie sposobu bezpiecznego
przesyłania żądań (takich jak informacje uwierzytelniające) między
stronami. Szkielet JOSE udostępnia zbiór specyfikacji służących temu
celowi.

%package -n python3-jose
Summary:	JOSE implementation in Python
Summary(pl.UTF-8):	Implementacja JOSE w Pythonie
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-jose
JOSE is a framework intended to provide a method to securely transfer
claims (such as authorization information) between parties. The JOSE
framework provides a collection of specifications to serve this
purpose.

%description -n python3-jose -l pl.UTF-8
JOSE to szkielet mający na celu zapewnienie sposobu bezpiecznego
przesyłania żądań (takich jak informacje uwierzytelniające) między
stronami. Szkielet JOSE udostępnia zbiór specyfikacji służących temu
celowi.

%package apidocs
Summary:	API documentation for Python jose module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona jose
Group:		Documentation

%description apidocs
API documentation for Python jose module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona jose.

%prep
%setup -q -n python-jose-%{version}
%patch0 -p1

# Sphinx 1.3+ ships napoleon extension in sphinx.ext namespace
%{__sed} -i -e 's/sphinxcontrib\.napoleon/sphinx.ext.napoleon/' docs/conf.py

%{__rm} -r tests/__pycache__ tests/*/__pycache__
%{__rm} tests/*.pyc tests/*/*.pyc

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin \
%{__python} -m pytest tests -k 'not test_key_too_short'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin \
%{__python3} -m pytest tests -k 'not test_key_too_short and not test_to_dict'
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py_sitescriptdir}/jose
%{py_sitescriptdir}/python_jose-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-jose
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/jose
%{py3_sitescriptdir}/python_jose-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,jwk,jws,jwt,*.html,*.js}
%endif
