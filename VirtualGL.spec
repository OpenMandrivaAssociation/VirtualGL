%define name    VirtualGL
%define version 2.3
%define release 1

Name:           %{name}
Summary:        A toolkit for displaying OpenGL applications to thin clients
Version:        %{version}
Release:        %{release}
Source0:        http://prdownloads.sourceforge.net/virtualgl/%{name}-%{version}.tar.gz
Patch0:         vgl_2.3_patch0
URL:            http://www.virtualgl.org

Group:          Networking/Other
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:        wxWindows Library License v3.1

BuildRequires: cmake gcc-c++ glibc-devel libjpeg-static-devel X11-devel

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
Summary: A toolkit for displaying OpenGL applications to thin clients
Group: Networking/Other
Requires: %{name} = %{version}

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

%prep
%setup -q
%patch0 -p1

%build
cmake -G "Unix Makefiles" -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} -DCMAKE_INSTALL_PREFIX=%{buildroot}/%{_prefix} -DTJPEG_INCLUDE_DIR=%{_includedir} -DTJPEG_LIBRARY=%{_libdir}/libturbojpeg.a .
%make

#make

%install
rm -rf %{buildroot}
%makeinstall
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
rm -rf %{buildroot}/%{_libdir}/fakelib
rm -rf %{buildroot}/%{_prefix}/fakelib
mkdir -p %{buildroot}/%{_libdir}/fakelib
ln -sf ../librrfaker.so %{buildroot}/%{_libdir}/fakelib/libGL.so
mv -f %{buildroot}/%{_bindir}/glxinfo %{buildroot}/%{_bindir}/glxinfo2

%clean
rm -rf %{buildroot}

%post
ldconfig

%postun
ldconfig

%files
%defattr(-,root,root)
%doc /usr/doc/*
%dir %{_libdir}/fakelib
%{_bindir}/*
%{_libdir}/fakelib/libGL.so
%{_libdir}/librrfaker.so
%{_libdir}/libdlfaker.so
%{_libdir}/libgefaker.so

%files devel
%defattr(-,root,root)
%{_includedir}/rrtransport.h
%{_includedir}/rr.h

