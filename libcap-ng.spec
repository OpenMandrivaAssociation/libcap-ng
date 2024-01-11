%define _disable_ld_no_undefined 1
%bcond_with crosscompile

%define major 0
%define libname %mklibname cap-ng
%define oldlibname %mklibname cap-ng 0
%define libdrop %mklibname drop_ambient
%define oldlibdrop %mklibname drop_ambient %{major}
%define devname %mklibname cap-ng -d

Summary:	An alternate posix capabilities library
Name:		libcap-ng
Version:	0.8.4
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://people.redhat.com/sgrubb/libcap-ng
Source0:	http://people.redhat.com/sgrubb/libcap-ng/%{name}-%{version}.tar.gz
Patch0:		https://src.fedoraproject.org/rpms/libcap-ng/raw/rawhide/f/libcap-ng-0.8.5-python-exception.patch
BuildRequires:	kernel-headers
BuildRequires:	swig
BuildRequires:	pkgconfig(libattr)
BuildRequires:	pkgconfig(python3)
# Using slibtool avoids the nasty libtool relink bug
# during make install when crosscompiling.
# And it's faster anyway.
BuildRequires:	slibtool
# libcap-ng likes building python2 bindings if it can...
BuildConflicts:	python2

%description
Libcap-ng is a library that makes using posix capabilities easier.

%package utils
Summary:	Utilities for analysing and setting file capabilities
Group:		System/Base

%description utils
The libcap-ng-utils package contains applications to analyse the posix
capabilities of all the program running on a system. It also lets you set the
file system based capabilities.

%package -n %{libname}
Summary:	Shared %{name} library
Group:		System/Libraries
%rename %oldlibname

%description -n	%{libname}
This package contains the shared %{name} library.

%package -n %{libdrop}
Summary:	Shared %{name} library
Requires:	%{libname} = %{EVRD}
Group:		System/Libraries
%rename oldlibdrop

%description -n	%{libdrop}
This package contains the shared %{name} library.

%package -n %{devname}
Summary:	Header files, libraries and development documentation for %{name}
Group:		Development/C
Requires:	kernel-headers
Requires:	%{libname} = %{EVRD}
Requires:	%{libdrop} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
This package contains the development files for the %{name} library.

%if !%{with crosscompile}
%package -n python-%{name}
Summary:	Python bindings for %{name} library
Group:		Development/Python
Requires:	%{libname} = %{EVRD}

%description -n	python-%{name}
The libcap-ng-python package contains the bindings so that %{name} and
can be used by python applications.
%endif

%prep
%autosetup -p1
autoreconf -fi

%build
%configure \
%if !%{with crosscompile}
	--with-python3
%else
	--without-python
%endif

%make_build LIBTOOL=slibtool-shared

%install
%make_install LIBTOOL=slibtool-shared

# Remove a couple things so they don't get picked up
rm -rf %{buildroot}/%{_libdir}/python%{py_ver}/site-packages/__pycache__

%files utils
%doc COPYING
%{_bindir}/*
%doc %{_mandir}/man8/*
%doc %{_mandir}/man7/*

%files -n %{libname}
%{_libdir}/libcap-ng.so.%{major}*

%files -n %{libdrop}
%{_libdir}/libdrop_ambient.so.%{major}*

%files -n %{devname}
%doc COPYING.LIB
%{_includedir}/cap-ng.h
%{_libdir}/libcap-ng.so
%{_libdir}/libdrop_ambient.so
%{_datadir}/aclocal/cap-ng.m4
%{_libdir}/pkgconfig/libcap-ng.pc
%doc %{_mandir}/man3/*

%if !%{with crosscompile}
%files -n python-%{name}
%{_libdir}/python%{py_ver}/site-packages/_capng.so
%{python3_sitearch}/capng.py*
%endif
