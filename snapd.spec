%if 0%{?fedora} || 0%{?rhel} == 6
%global with_devel 1
%global with_bundled 0
%global with_debug 1
%global with_check 0
%global with_unit_test 0
%else
%global with_devel 0
%global with_bundled 0
%global with_debug 0
%global with_check 0
%global with_unit_test 0
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         snapcore
%global repo            snapd
# https://github.com/snapcore/snapd
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}

Name:           snapd
Version:        2.11
Release:        1%{?dist}
Summary:        The snapd and snap tools enable systems to work with .snap files
License:        GPL-3
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{version}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
# BuildRequires:  systemd-units
BuildRequires:  systemd
%{?systemd_requires}
Requires:       snap-confine
Requires:       squashfs-tools
# we need squashfs.ko loaded
Requires:       kernel-modules

%if ! 0%{?with_bundled}
BuildRequires: golang(github.com/cheggaaa/pb)
BuildRequires: golang(github.com/coreos/go-systemd/activation)
BuildRequires: golang(github.com/gorilla/context)
BuildRequires: golang(github.com/gorilla/mux)
BuildRequires: golang(github.com/gorilla/websocket)
BuildRequires: golang(github.com/gosexy/gettext)
BuildRequires: golang(github.com/jessevdk/go-flags)
BuildRequires: golang(github.com/mvo5/goconfigparser)
BuildRequires: golang(github.com/mvo5/uboot-go/uenv)
BuildRequires: golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: golang(gopkg.in/check.v1)
BuildRequires: golang(gopkg.in/tomb.v2)
BuildRequires: golang(gopkg.in/yaml.v2)
BuildRequires: golang(gopkg.in/macaroon.v1)
%endif

%description
Snappy is a modern, cross-distribution, transactional package manager designed for
working with self-contained, immutable packages.

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
%endif

Provides:      golang(%{import_path}) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{name}-%{version}

%build
mkdir -p src/github.com/snapcore
ln -s ../../../ src/github.com/snapcore/snapd

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

%gobuild -o bin/snap %{import_path}/cmd/snap
%gobuild -o bin/snap-exec %{import_path}/cmd/snap-exec
%gobuild -o bin/snapd %{import_path}/cmd/snapd


%install
install -d -p %{buildroot}%{_bindir}
install -d -p %{buildroot}%{_libexecdir}/snapd
install -d -p %{buildroot}%{_unitdir}
install -d -p %{buildroot}%{_prefix}/lib/systemd/system-preset
install -d -p %{buildroot}%{_sysconfdir}/profile.d

# Install snap and snapd
install -p -m 0755 bin/snap %{buildroot}%{_bindir}
install -p -m 0755 bin/snap-exec %{buildroot}%{_libexecdir}/snapd
install -p -m 0755 bin/snapd %{buildroot}%{_libexecdir}/snapd

# Install all systemd units
install -p -m 0644 debian/snapd.socket %{buildroot}%{_unitdir}
install -p -m 0644 debian/snapd.service %{buildroot}%{_unitdir}
install -p -m 0644 debian/snapd.refresh.service %{buildroot}%{_unitdir}
install -p -m 0644 debian/snapd.refresh.timer %{buildroot}%{_unitdir}
install -p -m 0644 debian/snapd.frameworks-pre.target %{buildroot}%{_unitdir}
install -p -m 0644 debian/snapd.frameworks.target %{buildroot}%{_unitdir}

# Patch debianism out of the service files
sed -i -e "s!/usr/lib/snapd/snapd!%{_libexecdir}/snapd/snapd!" %{buildroot}%{_unitdir}/snapd.service
sed -i -e "s!/usr/bin/snap!%{_bindir}/snap!" %{buildroot}%{_unitdir}/snapd.refresh.service

# Install systemd preset for running snapd
cat << __SNAPD_PRESET__ > %{buildroot}%{_prefix}/lib/systemd/system-preset/91-snapd.preset
enable snapd.socket
enable snapd.service
enable snapd.refresh.timer
enable snapd.refresh.service
__SNAPD_PRESET__

# Put /snap/bin on PATH
# Put /var/lib/snpad/desktop on XDG_DATA_DIRS
cat << __SNAPD_SH__ > %{buildroot}%{_sysconfdir}/profile.d/snapd.sh
PATH=$PATH:/snap/bin
if [ -z "$XDG_DATA_DIRS" ]; then
    XDG_DATA_DIRS=/usr/local/share/:/usr/share/:/var/lib/snapd/desktop
else
    XDG_DATA_DIRS="$XDG_DATA_DIRS":/var/lib/snapd/desktop
fi
export XDG_DATA_DIRS
__SNAPD_SH__

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/Godeps/_workspace:%{gopath}
%endif
%gotest %{import_path}
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license COPYING 
%doc README.md
%{_bindir}/snap
%{_libexecdir}/snapd
%{_sysconfdir}/profile.d/snapd.sh
%{_prefix}/lib/systemd/system-preset/91-snapd.preset
%{_unitdir}/snapd.socket
%{_unitdir}/snapd.service
%{_unitdir}/snapd.frameworks-pre.target
%{_unitdir}/snapd.frameworks.target
%{_unitdir}/snapd.refresh.service
%{_unitdir}/snapd.refresh.timer


%if 0%{?with_devel}
%files devel -f devel.file-list
%license COPYING
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license COPYING
%doc README.md
%endif

%post
%systemd_post snapd.service snapd.socket snapd.refresh.timer snapd.refresh.service
if [ $1 -eq 1 ]; then
        systemctl start snapd.socket
        systemctl start snapd.refresh.timer
        modprobe squashfs
fi

%preun
%systemd_preun snapd.service snapd.socket snapd.refresh.timer snapd.refresh.service

%postun
%systemd_postun_with_restart snapd.service snapd.socket snapd.refresh.timer snapd.refresh.service
if [ $1 -eq 0 ]; then 
        # Remove all generated systemd mount units 
        find /etc/systemd/system -name "snap-*.mount" -delete
        # Remove all generated systemd service units 
        find /etc/systemd/system -name "snap*.service" -delete
        # Remove all symlinks to the two
        find /etc/systemd/system/multi-user.target.wants -name "snap-*.mount" -delete
        find /etc/systemd/system/multi-user.target.wants -name "snap*.service" -delete
        # Unmount all snaps
        if [ -n "$(mount | grep snap | awk '{print $3}')" ]; then
                umount --lazy $(mount | grep snap | awk '{print $3}')
        fi
        # Remove all generated snap launchers and miscellaneous files
        rm -rf /snap
        # Remove all snapd state
        rm -rf /var/lib/snapd
fi

%changelog
* Tue Aug 16 2016 Zygmunt Krynicki <me@zygoon.pl> - 2.11-1
- New upstream release
- Move private executables to /usr/libexec/snapd/
* Fri Jun 24 2016 Zygmunt Krynicki - 2.0.9-2
- Depend on kernel-modules to ensure that squashfs can be loaded. Load it afer
  installing the package. This hopefully fixes
  https://github.com/zyga/snapcore-fedora/issues/2
* Fri Jun 17 2016 Zygmunt Krynicki - 2.0.9
- New upstream release
  https://github.com/snapcore/snapd/releases/tag/2.0.9
* Tue Jun 14 2016 Zygmunt Krynicki - 2.0.8.1
- New upstream release
* Fri Jun 10 2016 Zygmunt Krynicki - 2.0.8
- First package for Fedora
