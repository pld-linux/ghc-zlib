#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	zlib
Summary:	Compression and decompression in the gzip and zlib formats
Summary(pl.UTF-8):	Kompresja i dekompresja formatów gzip i zlib
Name:		ghc-%{pkgname}
Version:	0.5.4.1
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/zlib
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	d0d10786d2bbd1d401a8b28a83e88475
URL:		http://hackage.haskell.org/package/zlib
BuildRequires:	ghc >= 6.12.3
%{?with_prof:BuildRequires:	ghc-prof >= 6.12.3}
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

%description
This package provides a pure interface for compressing and
decompressing streams of data represented as lazy 'ByteString's. It
uses the zlib C library so it has high performance. It supports the
"zlib", "gzip" and "raw" compression formats.

It provides a convenient high level API suitable for most tasks and
for the few cases where more control is needed it provides access to
the full zlib feature set.

%description -l pl.UTF-8
Ten pakiet zapewnia czysty interfejs do kompresji i dekompresji
strumieni danych reprezentowanych jako leniwe "ByteString"i.
Wykorzystuje bibliotekę C zlib, więc ma dużą wydajność. Obsługuje
formaty kompresji "zlib", "gzip" i "surowy".

Udostępnia wygodne, wysokopoziomowe API, nadające się do większości
zadań; dla nielicznych przypadków, gdzie potrzeba większej kontroli,
daje dostęp do pełnych możliwości zliba.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSzlib-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSzlib-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Compression
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Compression/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Compression/Zlib
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Compression/Zlib/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSzlib-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Compression/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Compression/Zlib/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
