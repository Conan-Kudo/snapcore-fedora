Name:       snap-confine
Version:    1.0.39
Release:    2%{?dist}
Summary:    Confinement system for snap applications

Group:      System Environment/Base
License:    GPLv3
URL:        https://github.com/snapcore/snap-confine
Source0:    https://github.com/snapcore/snap-confine/releases/download/%{version}/%{name}-%{version}.tar.gz
Patch0:		snap-confine-not-setuid.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  indent
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  python3-docutils
BuildRequires:  systemd-devel
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(udev)

%description
The package is used internally by snapd to apply confinement to the started
snap applications.


%prep
%setup -q
%patch0 -p1


%build
autoreconf --force --install --verbose
# selinux support is not yet available, for now just disable apparmor
%configure --disable-apparmor --libexecdir=%{_libexecdir}/snapd/
%make_build


%check
make check


%install
%make_install


%files
%doc README.md PORTING
%license COPYING
%attr(0755,root,root) %caps(cap_sys_admin=pe) %{_libexecdir}/snapd/snap-confine
%{_bindir}/ubuntu-core-launcher
%{_mandir}/man1/ubuntu-core-launcher.1.*
%{_mandir}/man5/snap-confine.5.*
%{_prefix}/lib/udev/snappy-app-dev
%{_udevrulesdir}/80-snappy-assign.rules


%changelog
* Wed Aug 17 2016 Zygmunt Krynicki <me@zygoon.pl> - 1.0.39-2
- Add the patch locally, not via sources
* Tue Aug 09 2016 Zygmunt Krynicki <me@zygoon.pl> - 1.0.39-1
- New upstream release
  https://github.com/snapcore/snap-confine/releases/tag/1.0.39
- Strip the setuid bit and use capabilities
- Use %%license instead of %%doc for COPYING
* Mon Jul 25 2016 Zygmunt Krynicki <me@zygoon.pl> - 1.0.38-1
- New upstream release
  https://github.com/snapcore/snap-confine/releases/tag/1.0.38
- Improve the packaging based on reviews
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
