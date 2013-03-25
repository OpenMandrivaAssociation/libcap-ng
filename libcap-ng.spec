%define	major 0
%define	libname %mklibname cap-ng %{major}
%define develname %mklibname cap-ng -d
%bcond_with	crosscompile

Summary:	An alternate posix capabilities library
Name:		libcap-ng
Version:	0.7.1
Release:	%mkrel 1
License:	LGPLv2+
Group:		System/Libraries
URL:		http://people.redhat.com/sgrubb/libcap-ng
Source0:	http://people.redhat.com/sgrubb/libcap-ng/%{name}-%{version}.tar.gz
BuildRequires:	kernel-headers >= 2.6.11
BuildRequires:	attr-devel
BuildRequires:	python-devel
BuildRequires:	swig

%description
Libcap-ng is a library that makes using posix capabilities easier.

%package -n	%{libname}
Summary:	Shared %{name} library
Group:		System/Libraries
Obsoletes:	%{_lib}libcap-ng0

%description -n	%{libname}
Libcap-ng is a library that makes using posix capabilities easier.

This package contains the shared %{name} library.

%package -n	%{develname}
Summary:	Header files, libraries and development documentation for %{name}
Group:		Development/C
Requires:	kernel-headers >= 2.6.11
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}libcap-ng-devel

%description -n	%{develname}
Libcap-ng is a library that makes using posix capabilities easier.

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

%package	utils
Summary:	Utilities for analysing and setting file capabilities
Group:		System/Base

%description	utils
The libcap-ng-utils package contains applications to analyse the posix
capabilities of all the program running on a system. It also lets you set the
file system based capabilities.

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

%make

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

%files -n %{libname}
%doc COPYING.LIB
%attr(0755,root,root) /%{_lib}/libcap-ng.so.%{major}*

%files -n %{develname}
%attr(0644,root,root) %{_includedir}/cap-ng.h
%attr(0755,root,root) %{_libdir}/libcap-ng.so
%attr(0644,root,root) %{_datadir}/aclocal/cap-ng.m4
%{_libdir}/pkgconfig/libcap-ng.pc
%attr(0644,root,root) %{_mandir}/man3/*

%if !%{with crosscompile}
%files -n python-%{name}
%attr(0755,root,root) /%{_libdir}/python?.?/site-packages/_capng.so
%{python_sitearch}/capng.py*
%endif

%files utils
%doc COPYING
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man8/*
