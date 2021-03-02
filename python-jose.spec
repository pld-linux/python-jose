#
# Conditional build:
%bcond_with	tests	# unit tests (not included in sdist)

Summary:	An implementation of the JOSE draft
Summary(pl.UTF-8):	Implementacja szkicu JOSE
Name:		python-jose
Version:	1.0.0
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jose/
Source0:	https://files.pythonhosted.org/packages/source/j/jose/jose-%{version}.tar.gz
# Source0-md5:	6fd62972b02965fb0151c1173e2e4a60
URL:		https://pypi.org/project/jose/
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-Crypto >= 2.6
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.5
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

%prep
%setup -q -n jose-%{version}

%build
%py_build

%if %{with tests}
%{__python} -m unittest ...
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES CONTRIB LICENSE
%attr(755,root,root) %{_bindir}/jose
%{py_sitescriptdir}/jose.py[co]
%{py_sitescriptdir}/jose-%{version}-py*.egg-info
