%define	major 0
%define	libname %mklibname cap-ng %{major}
%define develname %mklibname cap-ng -d

Summary:	An alternate posix capabilities library
Name:		libcap-ng
Version:	0.6.5
Release:	%mkrel 2
License:	LGPLv2+
Group:		System/Libraries
URL:		http://people.redhat.com/sgrubb/libcap-ng
Source0:	http://people.redhat.com/sgrubb/libcap-ng/%{name}-%{version}.tar.gz
BuildRequires:	kernel-headers >= 2.6.11
BuildRequires:	attr-devel
BuildRequires:	python-devel
BuildRequires:	swig
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package -n	python-%{name}
Summary:	Python bindings for %{name} library
Group:		Development/Python
Requires:	%{libname} = %{version}-%{release}

%description -n	python-%{name}
The libcap-ng-python package contains the bindings so that %{name} and
can be used by python applications.

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
    --with-python

%make

%install
rm -rf %{buildroot}

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

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun	-n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root,-)
%doc COPYING.LIB
%attr(0755,root,root) /%{_lib}/libcap-ng.so.%{major}*

%files -n %{develname}
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/cap-ng.h
%attr(0755,root,root) %{_libdir}/libcap-ng.so
%attr(0644,root,root) %{_datadir}/aclocal/cap-ng.m4
%{_libdir}/pkgconfig/libcap-ng.pc
%attr(0644,root,root) %{_mandir}/man3/*

%files -n python-%{name}
%defattr(-,root,root,-)
%attr(0755,root,root) /%{_libdir}/python?.?/site-packages/_capng.so
%{python_sitearch}/capng.py*

%files utils
%defattr(-,root,root,-)
%doc COPYING
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man8/*
