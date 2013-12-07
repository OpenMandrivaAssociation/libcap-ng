%define _disable_ld_no_undefined 1
%bcond_with	crosscompile

%define	major	0
%define	libname	%mklibname cap-ng %{major}
%define devname	%mklibname cap-ng -d

Summary:	An alternate posix capabilities library
Name:		libcap-ng
Version:	0.7.3
Release:	4
License:	LGPLv2+
Group:		System/Libraries
Url:		http://people.redhat.com/sgrubb/libcap-ng
Source0:	http://people.redhat.com/sgrubb/libcap-ng/%{name}-%{version}.tar.gz
BuildRequires:	kernel-headers >= 2.6.11
BuildRequires:	swig
BuildRequires:	attr-devel
BuildRequires:	pkgconfig(python)

%description
Libcap-ng is a library that makes using posix capabilities easier.

%package	utils
Summary:	Utilities for analysing and setting file capabilities
Group:		System/Base

%description	utils
The libcap-ng-utils package contains applications to analyse the posix
capabilities of all the program running on a system. It also lets you set the
file system based capabilities.

%package -n	%{libname}
Summary:	Shared %{name} library
Group:		System/Libraries

%description -n	%{libname}
This package contains the shared %{name} library.

%package -n	%{devname}
Summary:	Header files, libraries and development documentation for %{name}
Group:		Development/C
Requires:	kernel-headers >= 2.6.11
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the development files for the %{name} library.

%if !%{with crosscompile}
%package -n	python-%{name}
Summary:	Python bindings for %{name} library
Group:		Development/Python
Requires:	%{libname} = %{version}-%{release}

%description -n	python-%{name}
The libcap-ng-python package contains the bindings so that %{name} and
can be used by python applications.
%endif

%prep
%setup -q

%build
%configure2_5x \
	--libdir=/%{_lib} \
%if !%{with crosscompile}
	--with-python
%else
	--without-python 
%endif

%install
%makeinstall_std

# Move the symlink
rm -f %{buildroot}/%{_lib}/%{name}.so
mkdir -p %{buildroot}%{_libdir}
VLIBNAME=$(ls %{buildroot}/%{_lib}/%{name}.so.*.*.*)
LIBNAME=$(basename $VLIBNAME)
ln -s ../../%{_lib}/$LIBNAME %{buildroot}%{_libdir}/%{name}.so

# Move the pkgconfig file
mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}

# Remove a couple things so they don't get picked up
rm -f %{buildroot}/%{_lib}/libcap-ng.*a
rm -f %{buildroot}/%{_libdir}/python?.?/site-packages/_capng.*a

%files utils
%doc COPYING
%{_bindir}/*
%{_mandir}/man8/*

%files -n %{libname}
/%{_lib}/libcap-ng.so.%{major}*

%files -n %{devname}
%doc COPYING.LIB
%{_includedir}/cap-ng.h
%{_libdir}/libcap-ng.so
%{_datadir}/aclocal/cap-ng.m4
%{_libdir}/pkgconfig/libcap-ng.pc
%{_mandir}/man3/*

%if !%{with crosscompile}
%files -n python-%{name}
/%{_libdir}/python?.?/site-packages/_capng.so
%{python_sitearch}/capng.py*
%endif

