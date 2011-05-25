%define name 	cheops-ng
%define version 0.2.3
%define release %mkrel 6

Summary:	Multipurpose network exploration tool
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/Other
Source0:	%{name}-%{version}.tar.bz2
Source1:	cheops-agent.bz2
#Patch0:		%{name}-0.1.10-Makefile.in-patch.bz2
Patch1:		%{name}-errno.patch.bz2
Patch2:		cheops-ng-0.2.3-use-size_t-for-storing-pointer.patch
URL:		http://cheops-ng.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gtk+-devel = 1.2.10 bison flex gnome-libs-devel ORBit-devel = 0.5.17
BuildRequires:	glib-devel = 1.2.10 libxml-devel xpm-devel nmap imlib-devel => 1.9.14
Requires:	nmap
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description
Cheops-ng is a Network management tool for mapping and monitoring your network.
It has host/network discovery functionality as well as OS detection of hosts. 
Cheops-ng has the ability to probe hosts to see what services they are running.
On some services, cheops-ng is actually able to see what program is running for
a service and the version number of that program.

NB: Run cheops-agent as root to enable the backend.

%prep
%setup -q

#%patch0 -p0
%patch1 -p1
%patch2 -p1 -b .64bit~

%build

# configure macro does not work
CFLAGS="%{optflags}" \
./configure	--prefix=%{_prefix} \
		--host=%{_target_platform} \
# make -j2 does not work
make XCFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
# makeinstall macro does not work
DEFAULTDIR="%{_datadir}/pixmaps/%{name}"

mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/${DEFAULTDIR}/pixmaps/

cp pixmaps/%{name}.xpm %{buildroot}/%{_datadir}/pixmaps/%name/pixmaps/
cp pixmaps/*.xpm %{buildroot}/${DEFAULTDIR}/pixmaps/

cp %{name} %{buildroot}/%{_bindir}
cp cheops-agent %{buildroot}/%{_bindir}

bzcat %{SOURCE1} > %{buildroot}%{_initrddir}/cheops-agent

# Menu
#?package(%{name}): needs="x11" \
#		    section="Documentation/Websites" \
#		    title="Cheops-NG Homepage" \
#		    command="if ps U \$USER | grep -q \$BROWSER; then \$BROWSER -remote \'openURL(%{url})\'; else \$BROWSER \'%{url}\'; fi" \
#		    icon="networking_section.png"
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_bindir}/%{name}
Icon=networking_section
Categories=Network;
Name=Cheops-NG
Comment=Network Browser and Tools (requires running agent)
EOF

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 200900
%{update_menus}
%endif
%_post_service cheops-agent

%preun
%_preun_service cheops-agent

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README doc/*
%{_bindir}/cheops-*
%attr(755,root,root) %config(noreplace) %{_initrddir}/cheops-agent
#%{_datadir}/pixmaps/*.xpm
%{_datadir}/pixmaps/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop

