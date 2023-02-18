#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_with	mpi		# MPI support

Summary:	Lunchbox - C++ library for multi-threading programming
Summary(pl.UTF-8):	Lunchbox - biblioteka C++ do programowania wielowątkowego
Name:		Lunchbox
Version:	1.17.0
Release:	7
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://github.com/Eyescale/Lunchbox/releases
Source0:	https://github.com/Eyescale/Lunchbox/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	76bcd79003c9b9d58d5f772cfdd812c7
Patch0:		cxx.patch
Patch1:		nanosleep.patch
URL:		http://pogl.wordpress.com/category/lunchbox/
BuildRequires:	Eyescale-CMake >= 2018.02
BuildRequires:	Servus-devel >= 1.5.0
BuildRequires:	avahi-devel
BuildRequires:	boost-devel >= 1.41.0
BuildRequires:	cmake >= 3.1
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	hwloc-devel >= 1.3
BuildRequires:	hwloc-devel < 2
BuildRequires:	libstdc++-devel
%{?with_mpi:BuildRequires:	mpi-devel}
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
Requires:	Servus >= 1.5.0
Requires:	hwloc-libs >= 1.3
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
Requires:	Servus-devel >= 1.5.0
Requires:	boost-devel >= 1.41.0
Requires:	libstdc++-devel

%description devel
Header files for Lunchbox library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Lunchbox.

%package apidocs
Summary:	Lunchbox API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Lunchbox
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Lunchbox library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Lunchbox.

%prep
%setup -q

rmdir CMake/common
ln -s %{_datadir}/Eyescale-CMake CMake/common

%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake .. \
	-DCOMMON_DISABLE_WERROR:BOOL=ON \
	%{!?with_mpi:-DCMAKE_DISABLE_FIND_PACKAGE_MPI=ON}

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
%attr(755,root,root) %ghost %{_libdir}/libLunchbox.so.10
%dir %{_datadir}/Lunchbox
%{_datadir}/Lunchbox/benchmarks

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libLunchbox.so
%{_includedir}/lunchbox
%{_datadir}/Lunchbox/CMake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif
