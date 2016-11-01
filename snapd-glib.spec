Name:		snapd-glib
Version:	1.2
Release:	1%{?dist}
Summary:	Library providing a GLib interface to snapd

Group:		System Environment/Libraries
License:	LGPLv2 or LGPLv3
URL:		https://launchpad.net/%{name}
Source0:	https://launchpad.net/%{name}/1.x/%{version}/+download/%{name}-%{version}.tar.xz

BuildRequires:	gtk-doc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gobject-introspection-devel
BuildRequires:  intltool
BuildRequires:  libtool 
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  vala-tools

%description
%{name} is a library that provides an interface to communicate
with snapd.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides the files for developing applications
that use %{name} to communicate with snapd.

%package -n snapd-login-service
Summary:        Service to allow non-root access to snapd
Group:          System Environment/Daemons
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       snapd
Requires:       polkit

%description -n snapd-login-service
Snapd Login Service is a daemon that allows users to request
authorization from snapd. It uses Polkit to check for permissions.

%prep
%setup -q


%build
autoreconf --force --install --verbose
%configure --enable-gtk-doc --libexecdir=%{_libexecdir}/snapd
%make_build


%install
%make_install

find %{buildroot} -name "*.la" -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license COPYING.LGPL2 COPYING.LGPL3
%doc NEWS
%{_libdir}/libsnapd-glib.so.*
%{_libdir}/girepository-1.0/Snapd-1.typelib

%files devel
%doc %{_datadir}/gtk-doc/html/snapd-glib
%{_includedir}/snapd-glib
%{_libdir}/libsnapd-glib.so
%{_libdir}/pkgconfig/snapd-glib.pc
%{_datadir}/vala/vapi/snapd-glib.*
%{_datadir}/gir-1.0/Snapd-1.gir

%files -n snapd-login-service
%{_libexecdir}/snapd/snapd-login-service
%{_sysconfdir}/dbus-1/system.d/io.snapcraft.SnapdLoginService.conf
%{_datadir}/dbus-1/interfaces/io.snapcraft.SnapdLoginService.xml
%{_datadir}/dbus-1/system-services/io.snapcraft.SnapdLoginService.service
%{_datadir}/polkit-1/actions/io.snapcraft.SnapdLoginService.policy

%changelog
* Tue Nov 1 2016  Zygmunt Krynicki <me@zygoon.pl> - 1.2-1
- Update to latest upstream release
* Tue Sep 27 2016 Neal Gompa <ngompa13@gmail.com> - 0.14-1
- Flesh out spec and add subpackages for devel and login service
* Thu Sep 08 2016 Zygmunt Krynicki <me@zygoon.pl> - 0.14-0
- Update to 0.14 
* Fri Aug 26 2016 Zygmunt Krynicki <me@zygoon.pl> - 0.8-1
- Initial version of the package
