#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_with	mpi		# MPI support
%bcond_with	skv		# SKV (Scalable Key-Value Store) support

Summary:	Lunchbox - C++ library for multi-threading programming
Summary(pl.UTF-8):	Lunchbox - biblioteka C++ do programowania wielowątkowego
Name:		Lunchbox
Version:	1.15.0
Release:	2
License:	LGPL v2.1
Group:		Libraries
Source0:	https://github.com/Eyescale/Lunchbox/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5d36a9eb706ab65572fd208574c187a2
Patch2:		cxx.patch
URL:		http://pogl.wordpress.com/category/lunchbox/
BuildRequires:	Eyescale-CMake >= 2016.04
BuildRequires:	Servus-devel >= 1.5.0
BuildRequires:	avahi-devel
BuildRequires:	boost-devel >= 1.41.0
BuildRequires:	cmake >= 2.8
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	gcc-c++ >= 6:4.2
BuildRequires:	hwloc-devel >= 1.3
BuildRequires:	leveldb-devel
BuildRequires:	libgomp-devel
BuildRequires:	libjpeg-turbo-devel >= 1.2.1
BuildRequires:	libstdc++-devel
%{?with_mpi:BuildRequires:	mpi-devel}
BuildRequires:	pkgconfig
%{?with_skv:BuildRequires:	skv-devel}
Requires:	hwloc-libs >= 1.3
Requires:	libjpeg-turbo >= 1.2.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lunchbox is a C++ library for multi-threaded programming. Lunchbox was
formerly known as eq::base or co::base, the foundation for the
Equalizer parallel rendering framework and the Collage network
library. It is intended for all application developers creating
high-performance multi-threaded programs.

%description -l pl.UTF-8
Lunchbox to biblioteka C++ do programowania wielowątkowego. Wcześniej
była znana jako eq::base lub co::base - podstawa szkieletu do
renderowania wielowątkowego Equalizer lub biblioteki sieciowej
Collage. Biblioteka jest przeznaczona dla wszystkich programistów
tworzących wysoko wydajne, wielowątkowe aplikacje.

%package devel
Summary:	Header files for Lunchbox library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Lunchbox
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel >= 1.41.0
Requires:	libgomp-devel
Requires:	libstdc++-devel

%description devel
Header files for Lunchbox library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Lunchbox.

%package apidocs
Summary:	Lunchbox API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Lunchbox
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Lunchbox library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Lunchbox.

%prep
%setup -q

ln -s %{_datadir}/Eyescale-CMake CMake/common
%{__rm} .gitexternals

%patch2 -p1

%build
install -d build
cd build
%cmake .. \
	-DBUILDYARD_DISABLED=ON \
	-DCOMMON_DISABLE_WERROR:BOOL=ON \
	%{!?with_mpi:-DCMAKE_DISABLE_FIND_PACKAGE_MPI=ON} \
	%{!?with_skv:-DCMAKE_DISABLE_FIND_PACKAGE_skv=ON}
%{__make}

%if %{with apidocs}
doxygen doc/Doxyfile
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/Lunchbox/{doc,tests}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ACKNOWLEDGEMENTS.txt AUTHORS.txt CHANGES.txt LICENSE.txt README.md doc/Changelog.md
%attr(755,root,root) %{_libdir}/libLunchbox.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libLunchbox.so.8

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libLunchbox.so
%{_includedir}/lunchbox
%dir %{_datadir}/Lunchbox
%{_datadir}/Lunchbox/CMake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif
