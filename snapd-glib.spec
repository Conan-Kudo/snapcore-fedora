Name:		snapd-glib
Version:	0.14
Release:	1%{?dist}
Summary:	Library providing a GLib interface to snapd.

Group:		Development/Libraries
License:	LGPLv2 or LGPLv3
URL:		https://launchpad.net/%{name}
Source0:	https://launchpad.net/%{name}/0.x/%{version}/+download/%{name}-%{version}.tar.xz

BuildRequires:	gtk-doc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gobject-introspection-devel
BuildRequires:  libtool 
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  vala-tools

%description


%prep
%setup -q


%build
autoreconf --force --install --verbose
%configure
make %{?_smp_mflags}


%install
%make_install


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license COPYING.LGPL2 COPYING.LGPL3
%doc



%changelog
* Thu Sep 08 2016 Zygmunt Krynicki <me@zygoon.pl> - 0.14-1
- Update to 0.14 
* Fri Aug 26 2016 Zygmunt Krynicki <me@zygoon.pl> - 0.8-1
- Initial version of the package
