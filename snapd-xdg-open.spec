Name:       snapd-xdg-open
Version:    0.0.0 
Release:    1%{?dist}
Summary:    DBus-based bridge for xdg-open within used by snap applications

Group:      System Environment/Base
License:    GPLv3
URL:        https://github.com/ubuntu-core/snapd-xdg-open
Source0:    https://github.com/ubuntu-core/snapd-xdg-open/releases/download/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  pkgconfig(glib-2.0)

%description
A D-Bus-activated helper service allowing snaps to launch URLs on the host
where its installed. The service validates and checks the requested URLs before
allowing them to be opened.


%prep
%setup -q


%build
autoreconf --force --install --verbose
%configure --libexecdir=%{_libexecdir}/snapd/
%make_build


%check
make check


%install
%make_install


%files
%license COPYING
%{_libexecdir}/snapd/snapd-xdg-open
%{_datadir}/dbus-1/services/com.canonical.SafeLauncher.service

%changelog
* Tue Aug 23 2016 Zygmunt Krynicki <me@zygoon.pl> - 0.0.0-1
- Initial version of the package
