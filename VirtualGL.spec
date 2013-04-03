%define libpackage %mklibname %{name}

Name:		VirtualGL
Summary:	A toolkit for displaying OpenGL applications to thin clients
Version:	2.3.2
Release:	1
Group:		Networking/Other
License:	wxWindows Library License v3.1
URL:		http://www.virtualgl.org
Source0:	http://prdownloads.sourceforge.net/virtualgl/%{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	glibc-devel
BuildRequires:	jpeg-static-devel
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
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
%setup -q

%build
cmake -G "Unix Makefiles" \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
	-DCMAKE_INSTALL_PREFIX=%{buildroot}/%{_prefix} \
	-DVGL_DOCDIR=%{_defaultdocdir}/%{name} \
	-DVGL_LIBDIR=%{_libdir} \
	-DTJPEG_INCLUDE_DIR=%{_includedir} \
	-DTJPEG_LIBRARY=%{_libdir}/libturbojpeg.a .
%make

%install
rm -rf %{buildroot}
%makeinstall

%ifarch x86_64
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
%endif

rm -rf %{buildroot}%{_libdir}/fakelib
rm -rf %{buildroot}%{_prefix}/fakelib
mkdir -p %{buildroot}%{_libdir}/fakelib
ln -sf ../librrfaker.so %{buildroot}%{_libdir}/fakelib/libGL.so
mv -f %{buildroot}%{_bindir}/glxinfo %{buildroot}%{_bindir}/glxinfo2

%files
%doc /usr/doc/*
%{_bindir}/*

%files -n %{libpackage}
%dir %{_libdir}/fakelib
%{_libdir}/fakelib/libGL.so
%{_libdir}/librrfaker.so
%{_libdir}/libdlfaker.so
%{_libdir}/libgefaker.so

%files devel
%{_includedir}/rrtransport.h
%{_includedir}/rr.h


%changelog
* Wed Jan 18 2012 Александр Казанцев <kazancas@mandriva.org> 2.3-3
+ Revision: 762216
- Change hard requires 32bit libs to x86_64 to Suggests

* Wed Jan 18 2012 Александр Казанцев <kazancas@mandriva.org> 2.3-2
+ Revision: 762152
- fix requires. Drop devel, add libpackage. For x86_64 we still need 32 package together with x86_64
- Split package into a new lib package, to allow installing 32 and 64 bits libraries at the same time.
- %changelog

* Tue Jan 17 2012 Александр Казанцев <kazancas@mandriva.org> 2.3-1
+ Revision: 761936
- imported package VirtualGL
- imported package VirtualGL


* Mon Jan 16 2012 Jaron Viëtor <jaron@vietors.com> 2.3-1mdk
- Initial package
