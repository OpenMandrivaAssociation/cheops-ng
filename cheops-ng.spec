Summary:	Multipurpose network exploration tool
Name:		cheops-ng
Version:	0.2.3
Release:	9
License:	GPLv2+
Group:		Networking/Other
Url:		https://cheops-ng.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2
Source1:	cheops-agent
Patch0:		cheops-ng-0.2.3-ditch-in_addr_deepstruct.patch
Patch1:		cheops-ng-errno.patch
Patch2:		cheops-ng-0.2.3-ldflags.patch
# openSuSE patches
Patch11:	cheops-ng-missing_autoheader_templates.patch
Patch12:	cheops-ng-modernize_configure.patch
Patch13:	cheops-ng-use_external_libadns.patch
Patch14:	cheops-ng-rename_clog.patch
Patch15:	cheops-ng-pointer_int_casts.patch
Patch16:	cheops-ng-codecleanup.patch
Patch17:	cheops-ng-off_by_one.patch
Patch18:	cheops-ng-destdir.patch
Patch19:	cheops-ng-fix_desktop_file.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	nmap
BuildRequires:	adns-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	pkgconfig(glib)
BuildRequires:	pkgconfig(gtk+)
BuildRequires:	pkgconfig(imlib)
BuildRequires:	pkgconfig(libxml)
BuildRequires:	pkgconfig(ORBit)
BuildRequires:	pkgconfig(xpm)
Requires:	nmap

%description
Cheops-ng is a Network management tool for mapping and monitoring your network.
It has host/network discovery functionality as well as OS detection of hosts.
Cheops-ng has the ability to probe hosts to see what services they are running.
On some services, cheops-ng is actually able to see what program is running for
a service and the version number of that program.

NB: Run cheops-agent as root to enable the backend.

%files
%doc AUTHORS ChangeLog README doc/*
%{_bindir}/cheops-ng
%{_sbindir}/cheops-agent
%attr(755,root,root) %config(noreplace) %{_initrddir}/cheops-agent
%dir %{_datadir}/cheops-ng
%dir %{_datadir}/cheops-ng/pixmaps
%{_datadir}/cheops-ng/pixmaps/*.xpm
%{_datadir}/pixmaps/cheops-ng.xpm
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/gnome/apps/Internet/cheops-ng.desktop

#----------------------------------------------------------------------------

%prep
%setup -q

%patch1 -p1
%patch11 -p0 -b .template~
%patch12 -p0
%patch13 -p0
%patch14 -p0
%patch15 -p0
%patch16 -p0
%patch17 -p0
%patch18 -p0
%patch19 -p0

%patch0 -p1
%patch2 -p1 -b .ldflags~

rm -f Makefile
aclocal -I m4
autoheader -I m4
autoconf -I m4
# grf, too incompetent to fix automake mess properly...
cp %{_datadir}/automake-`automake --version|head -n1|cut -d\  -f4|cut -d. -f-2`/config.sub .

%build
%configure2_5x
# make -j2 does not work
make

%install
%makeinstall_std

install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/cheops-agent

mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_bindir}/%{name}
Icon=networking_section
Categories=Network;
Name=Cheops-NG
Comment=Network Browser and Tools (requires running agent)
EOF

