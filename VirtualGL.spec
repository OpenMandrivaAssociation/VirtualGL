# Work around incomplete debug packages
%global _empty_manifest_terminate_build 0

# Fix build with LLD 17
%global build_ldflags %{build_ldflags} -Wl,--undefined-version

%define libpackage %mklibname %{name}
%define Werror_cflags %nil
%define tarname	virtualgl

Name:		VirtualGL
Summary:	A toolkit for displaying OpenGL applications to thin clients
Version:	3.1
Release:	1
Group:		Networking/Other
License:	wxWindows Library License v3.1
URL:		http://www.virtualgl.org
Source0:	https://github.com/VirtualGL/virtualgl/archive/%{version}/%{tarname}-%{version}.tar.gz
# Use system glx.h
#Patch0:         faedcc1e36b4ed89a325e01822447900840a0b77.patch
# fix for bz923961
Patch1:         %{name}-redhatpathsfix.patch
# fix for bz1088475
Patch2:         %{name}-redhatlibexecpathsfix.patch
BuildRequires:	cmake
BuildRequires:	glibc-devel
BuildRequires:	fltk-devel
BuildRequires:	fltk-fluid
BuildRequires:	jpeg-static-devel
BuildRequires:	opencl-devel
BuildRequires:	opencl-headers
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xcb-keysyms)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
Requires:	%{libpackage} = %{version}

%description
VirtualGL is a library which allows most Linux OpenGL applications to be
remotely displayed to a thin client without the need to alter the
applications in any way.  VGL inserts itself into an application at run time
and intercepts a handful of GLX calls, which it reroutes to the server's
display (which presumably has a 3D accelerator attached.)  This causes all
3D rendering to occur on the server's display.  As each frame is rendered
by the server, VirtualGL reads back the pixels from the server's framebuffer
and sends them to the client for re-compositing into the appropriate X
Window.  VirtualGL can be used to give hardware-accelerated 3D capabilities to
VNC or other remote display environments that lack GLX support.  In a LAN
environment, it can also be used with its built-in motion-JPEG video delivery
system to remotely display full-screen 3D applications at 20+ frames/second.

VirtualGL is based upon ideas presented in various academic papers on
this topic, including "A Generic Solution for Hardware-Accelerated Remote
Visualization" (Stegmaier, Magallon, Ertl 2002) and "A Framework for
Interactive Hardware Accelerated Remote 3D-Visualization" (Engel, Sommer,
Ertl 2000.)

%package devel
Summary:	A toolkit for displaying OpenGL applications to thin clients
Group:		Networking/Other
Requires:	%{name} = %{version}

%description devel
VirtualGL is a library which allows most Linux OpenGL applications to be
remotely displayed to a thin client without the need to alter the
applications in any way.  VGL inserts itself into an application at run time
and intercepts a handful of GLX calls, which it reroutes to the server's
display (which presumably has a 3D accelerator attached.)  This causes all
3D rendering to occur on the server's display.  As each frame is rendered
by the server, VirtualGL reads back the pixels from the server's framebuffer
and sends them to the client for re-compositing into the appropriate X
Window.  VirtualGL can be used to give hardware-accelerated 3D capabilities to
VNC or other remote display environments that lack GLX support.  In a LAN
environment, it can also be used with its built-in motion-JPEG video delivery
system to remotely display full-screen 3D applications at 20+ frames/second.

VirtualGL is based upon ideas presented in various academic papers on
this topic, including "A Generic Solution for Hardware-Accelerated Remote
Visualization" (Stegmaier, Magallon, Ertl 2002) and "A Framework for
Interactive Hardware Accelerated Remote 3D-Visualization" (Engel, Sommer,
Ertl 2000.)

%package -n %{libpackage}
Summary:	Libraries injected by VirtualGL into applications that are ran through it
Group:		System/Libraries

%description -n %{libpackage}
Libraries injected by VirtualGL into applications that are ran throught it. 
Lib package allow installing 32 and 64 bits libraries at the same time.

%prep
%setup -qn virtualgl-%{version}
%autopatch -p1
sed -i -e 's,"glx.h",<GL/glx.h>,' server/*.[hc]*
sed -i -e 's,"glxext.h",<GL/glxext.h>,' server/*.[hc]*
rm doc/LICENSE-*.txt

# Use /var/lib, bug #428122
sed -e "s#/etc/opt#/var/lib#g" -i doc/unixconfig.txt doc/index.html doc/advancedopengl.txt \
	server/vglrun.in server/vglgenkey server/vglserver_config


%build
#export LDFLAGS="%{ldflags} -Wl,--no-as-needed"

cmake -G "Unix Makefiles" \
         -DVGL_SYSTEMFLTK=1 \
         -DVGL_SYSTEMGLX=1 \
         -DVGL_FAKEXCB=1 \
         -DVGL_USESSL=0 \
         -DVGL_BUILDSTATIC=0 \
         -DTJPEG_INCLUDE_DIR=%{_includedir}/ \
         -DTJPEG_LIBRARY=%{_libdir}/libturbojpeg.so \
         -DCMAKE_INSTALL_PREFIX=%{_prefix}/ \
         -DCMAKE_INSTALL_LIBDIR=%{_libdir}/VirtualGL/ \
         -DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name}/ \
         -DCMAKE_INSTALL_BINDIR=%{_bindir}/ .

%make_build

%install
%make_install

# glxinfo conflicts with command from glx-utils so lets do what Arch does
# and rename the command
mv $RPM_BUILD_ROOT/%{_bindir}/glxinfo $RPM_BUILD_ROOT/%{_bindir}/vglxinfo
mkdir -p $RPM_BUILD_ROOT%{_libdir}/fakelib/
ln -sf %{_libdir}/VirtualGL/librrfaker.so $RPM_BUILD_ROOT%{_libdir}/fakelib/libGL.so

%ifarch %{x86_64} aarch64 znver1
mv %{buildroot}%{_bindir}/.vglrun.vars64 %{buildroot}%{_bindir}/vglrun.vars64
%else
mv %{buildroot}%{_bindir}/.vglrun.vars32 %{buildroot}%{_bindir}/vglrun.vars32
%endif


%files
%{_docdir}/%{name}
%{_bindir}/*

%files -n %{libpackage}
%{_libdir}/fakelib/libGL.so
%{_libdir}/VirtualGL/libdlfaker.so
%{_libdir}/VirtualGL/libvglfaker-nodl.so
%{_libdir}/VirtualGL/libvglfaker.so
%{_libdir}/VirtualGL/libgefaker.so
%{_libdir}/VirtualGL/libvglfaker-opencl.so

%files devel
%{_includedir}/rrtransport.h
%{_includedir}/rr.h
