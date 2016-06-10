Name:		snap-confine
Version:	2.0
Release:	1%{?dist}
Summary:	Confinement system for snap applications

Group:		System Environment/Base
License:	GPLv3
URL:		https://github.com/ubuntu-core/snap-confine
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	indent
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc

%description
The package is used internally by snapd to apply confinement to the started
application process.


%prep
%setup -q


%build
autoreconf --force --install --verbose
# snapd uses seccomp and apparmor, selinux support is not yet available
%configure --disable-confinement --enable-rootfs-is-core-snap
make %{?_smp_mflags}


%install
%make_install
install -m 755 -d %{buildroot}/%{_libdir}
mv %{buildroot}/%{_bindir}/snap-confine %{buildroot}/%{_libdir}/


%files
%doc README.md PORTING
%attr(4755, root, root) %{_libdir}/snap-confine
%{_bindir}/*
%{_libdir}/*


%changelog
* Sat Jun 04 2016 Zygmunt Krynicki <me@zygoon.pl> - 2.0-1
- Initial version of the package
