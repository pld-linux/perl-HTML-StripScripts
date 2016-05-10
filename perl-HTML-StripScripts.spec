#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	HTML
%define	pnam	StripScripts
Summary:	HTML::StripScripts - Strip scripting constructs out of HTML
Summary(pl.UTF-8):	HTML::StripScripts - wyciągnij konstrukcje skryptowe poza HTML
Name:		perl-HTML-StripScripts
Version:	1.05
Release:	2
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/HTML/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	e8c51fbfda69efaf94c2937084d2458f
Patch0:		HTML-StripScripts-1.05-Fix-typo-in-regex.patch
URL:		http://search.cpan.org/dist/HTML-StripScripts/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module strips scripting constructs out of HTML, leaving as much
non-scripting markup in place as possible. This allows web
applications to display HTML originating from an untrusted source
without introducing XSS (cross site scripting) vulnerabilities.

You will probably use HTML::StripScripts::Parser rather than using
this module directly.

The process is based on whitelists of tags, attributes and attribute
values. This approach is the most secure against disguised scripting
constructs hidden in malicious HTML documents.

As well as removing scripting constructs, this module ensures that
there is a matching end for each start tag, and that the tags are
properly nested.

Previously, in order to customise the output, you needed to subclass
HTML::StripScripts and override methods. Now, most customisation can
be done through the Rules option provided to new(). (See
examples/declaration/ and examples/tags/ for cases where subclassing
is necessary.)

%description -l pl.UTF-8
Moduł ten wyciąga konstrukcje skryptowe poza HTML zastępując je
znacznikami nieskryptowymi w każdym możliwym miejscu. Dzięki temu
aplikacje webowe mogą wyświetlać HTML pochodzący z niezaufanego źródła
bez wprowadzania wrażliwości XSS (cross site scripting).

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorlib}/HTML/*.pm
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
