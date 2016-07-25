Name:		snap-confine
Version:	1.0.35
Release:	1%{?dist}
Summary:	Confinement system for snap applications

Group:		System Environment/Base
License:	GPLv3
URL:		https://github.com/snapcore/snap-confine
Source0:	https://github.com/snapcore/snap-confine/releases/download/%{version}/%{name}-%{version}.tar.gz

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc
BuildRequires:	glib2-devel
BuildRequires:	indent
BuildRequires:	libseccomp-devel
BuildRequires:	python3-docutils
BuildRequires:	systemd
BuildRequires:	systemd-devel

%description
The package is used internally by snapd to apply confinement to the started
snap applications.


%prep
%setup -q


%build
autoreconf --force --install --verbose
# selinux support is not yet available, for now just disable apparmor
%configure --disable-apparmor --enable-rootfs-is-core-snap --libdir=/usr/lib/snapd
make %{?_smp_mflags}


%check
make check


%install
%make_install


%files
%doc README.md PORTING
%attr(4755, root, root) %{_libexecdir}/snap-confine
%{_bindir}/*
%{_mandir}/*
/usr/lib/udev/rules.d/80-snappy-assign.rules
/usr/lib/udev/snappy-app-dev


%changelog
* Thu Jul 7 2016 Zygmunt Krynicki <me@zygoon.pl> - 1.0.35-1
- New upstream release
  https://github.com/snapcore/snap-confine/releases/tag/1.0.35
- Drop patch applied in the previous release
* Fri Jul 1 2016 Zygmunt Krynicki <me@zygoon.pl> - 1.0.34-2
- Apply 0001-Fix-check-for-CONFINEMENT_TESTS.patch to fix build issue on i386
* Fri Jul 1 2016 Zygmunt Krynicki <me@zygoon.pl> - 1.0.34-1
- New upstream release
  https://github.com/snapcore/snap-confine/releases/tag/1.0.34
* Tue Jun 21 2016 Zygmunt Krynicki <me@zygoon.pl> - 1.0.33-1
- New upstream release
  https://github.com/snapcore/snap-confine/releases/tag/1.0.33
* Mon Jun 20 2016 Zygmunt Krynicki <me@zygoon.pl> - 1.0.32-1
- New upstream release
  https://github.com/snapcore/snap-confine/releases/tag/1.0.32
* Thu Jun 16 2016 Zygmunt Krynicki <me@zygoon.pl> - 1.0.30-1
- New upstream release
- Make ubuntu-core-launcher a symlink to snap-confine
* Sat Jun 04 2016 Zygmunt Krynicki <me@zygoon.pl> - 1.0.29-1
- Initial version of the package
