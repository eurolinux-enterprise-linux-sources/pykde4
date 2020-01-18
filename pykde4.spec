%define pykde4_akonadi 1
%define pyqt4_version_min 4.9.5
%define sip_version_min 4.14
%if 0%{?fedora} > 17
%define python3 1
%endif
%if 0%{?fedora}
%define qscintilla 1
%define webkit 1
%endif

Name:    pykde4 
Version: 4.10.5
Release: 1%{?dist}
Summary: Python bindings for KDE4 

# http://techbase.kde.org/Policies/Licensing_Policy
License: LGPLv2+
URL:     http://developer.kde.org/language-bindings/
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

# See https://reviewboard.kde.org/r/101903
# hard-codes sip path to /usr/share/sip, instead of respecting system path
Patch1: 0001-Ensure-SIP-files-are-installed-to-the-right-path-bas.patch

## upstreamable patches

## upstream patches

# debian patches
Patch200: pykde4-4.9.90-respect_sip_flags.patch
Patch201: fix_kpythonpluginfactory_build.diff

# rhel patches
Patch300: pykde4-4.8.3-webkit.patch

BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: kdepimlibs-devel >= %{version}
BuildRequires: pkgconfig(akonadi)
%if 0%{?fedora} || 0%{?rhel} > 6
BuildRequires: pkgconfig(python)
%else
BuildRequires: python-devel
%endif
BuildRequires: pkgconfig(qimageblitz)
BuildRequires: pkgconfig(soprano)
%if 0%{?webkit}
BuildRequires: pkgconfig(QtWebKit)
BuildRequires: PyQt4-webkit-devel
%endif
BuildRequires: PyQt4-devel >= %{pyqt4_version_min}, sip-devel >= %{sip_version_min}
%if 0%{?python3}
BuildRequires: python3-devel
BuildRequires: python3-PyQt4-devel >= %{pyqt4_version_min}, python3-sip-devel >= %{sip_version_min}
%global python3_abiflags %(%{__python3} -c "import sys ; print (\\"%s\\" % (getattr(sys,'abiflags','')))")
%global python3_pyqt4_version %(%{__python3} -c 'import PyQt4.pyqtconfig; print(PyQt4.pyqtconfig._pkg_config["pyqt_version_str"])' 2> /dev/null || echo %{pyqt4_version_min})
%endif
%if 0%{?qscintilla}
BuildRequires: qscintilla-devel >= 2.4
%endif

Requires: kdelibs4%{?_isa} >= %{version}
Requires: kate-part%{?_isa} >= %{version}
%global pyqt4_version %(%{__python} -c 'import PyQt4.pyqtconfig; print(PyQt4.pyqtconfig._pkg_config["pyqt_version_str"])' 2> /dev/null || echo %{pyqt4_version_min})
Requires: PyQt4 >= %{pyqt4_version}
%if 0%{?webkit}
Requires: PyQt4-webkit
%endif
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}
%if ! 0%{?pykde4_akonadi}
Provides: PyKDE4-akonadi = %{version}-%{release}
Provides: PyKDE4-akonadi%{?_isa} = %{version}-%{release}
Provides: pykde4-akonadi% = %{version}-%{release}
Provides: pykde4-akonadi%{?_isa} = %{version}-%{release}
Requires: kdepimlibs-akonadi%{?_isa} >= %{version}
%endif

Obsoletes: PyKDE4 < 4.7.97-1
Provides:  PyKDE4 = %{version}-%{release}
Provides:  PyKDE4%{?_isa} = %{version}-%{release}

%description
%{summary}.

%package akonadi
Summary: Akonadi runtime support for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: kdepimlibs-akonadi%{?_isa} >= %{version} 
Obsoletes: PyKDE4-akonadi < 4.7.97-1 
Provides:  PyKDE4-akonadi = %{version}-%{release}
Provides:  PyKDE4-akonadi%{?_isa} = %{version}-%{release}
%description akonadi 
%{summary}.

%package devel
Summary:  Files needed to build %{name}-based applications
Requires: PyQt4-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%if 0%{?pykde4_akonadi}
Requires: %{name}-akonadi%{?_isa} = %{version}-%{release}
%endif
Obsoletes: PyKDE4-devel < 4.7.97-1
Provides:  PyKDE4-devel =  %{version}-%{release}
Provides:  PyKDE4-devel%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package -n python3-pykde4
Summary: Python 3 bindings for KDE 
Requires: python3-PyQt4 >= %{python3_pyqt4_version}
%{?_sip_api:Requires: python3-sip-api(%{_sip_api_major}) >= %{_sip_api}}
%if ! 0%{?pykde4_akonadi}
Provides: python3-pykde4-akonadi = %{version}-%{release}
Provides: python3-pykde4-akonadi%{?_isa} = %{version}-%{release}
Provides: python3-PyKDE4-akonadi = %{version}-%{release}
Provides: python3-PyKDE4-akonadi%{?_isa} = %{version}-%{release}
Requires: kdepimlibs-akonadi%{?_isa} >= %{version}
%endif
Obsoletes: python3-PyKDE4 < 4.7.97-1
Provides:  python3-PyKDE4 =  %{version}-%{release}
Provides:  python3-PyKDE4%{?_isa} = %{version}-%{release}
%description -n python3-pykde4
%{summary}.

%package -n python3-pykde4-akonadi
Summary: Akonadi runtime support for %{name} 
Requires: python3-PyKDE4%{?_isa} = %{version}-%{release}
Requires: kdepimlibs-akonadi%{?_isa} >= %{version}
Obsoletes: python3-PyKDE4-akonadi < 4.7.97-1
Provides:  python3-PyKDE4-akonadi =  %{version}-%{release}
Provides:  python3-PyKDE4-akonadi%{?_isa} = %{version}-%{release}
%description -n python3-pykde4-akonadi
%{summary}.

%package -n python3-pykde4-devel
Summary:  Files needed to build %{name}-based applications
Requires: python3-PyQt4-devel
Requires: python3-pykde4%{?_isa} = %{version}-%{release}
%if 0%{?pykde4_akonadi}
Requires: python3-pykde4-akonadi%{?_isa} = %{version}-%{release}
%endif
Obsoletes: python3-PyKDE4-devel < 4.7.97-1
Provides:  python3-PyKDE4-devel =  %{version}-%{release}
Provides:  python3-PyKDE4-devel%{?_isa} = %{version}-%{release}
%description -n python3-pykde4-devel
%{summary}.


%prep
%setup -q -n pykde4-%{version}

%patch1 -p1 -R -b .use_system_sip_dir

%patch200 -p1 -b .respect_sip_flags
%patch201 -p1 -b .kpythonpluginfactory_slots

%if ! 0%{?webkit}
%patch300 -p1 -b .webkit
%endif


%build
%if 0%{?python3}
mkdir -p %{_target_platform}-python3
pushd    %{_target_platform}-python3
%{cmake_kde4} \
  -DPYTHON_EXECUTABLE:PATH=%{__python3} \
  -DPYTHON_LIBRARY:PATH=%{_libdir}/libpython%{python3_version}%{?python3_abiflags}.so.1.0 \
  ..

make %{?_smp_mflags}
popd
%endif

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} \
  -DPYKDEUIC4_ALTINSTALL:BOOL=ON \
  -DPYTHON_EXECUTABLE:PATH=%{__python} \
  -DPYTHON_LIBRARY:PATH=%{_libdir}/libpython%{python_version}.so.1.0 \
  ..
  
make %{?_smp_mflags}
popd
 

%install
%if 0%{?python3}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}-python3

# not python3 compat yet
rm -fv %{buildroot}%{_kde4_libdir}/kde4/kpythonpluginfactory.so 

# HACK: fix multilib conflict, similar to PyQt4's http://bugzilla.redhat.com/509415
rm -fv %{buildroot}%{_bindir}/pykdeuic4-%{python3_version}
mv %{buildroot}%{python3_sitearch}/PyQt4/uic/pykdeuic4.py \
   %{buildroot}%{_bindir}/pykdeuic4-%{python3_version}
ln -s %{_bindir}/pykdeuic4-%{python3_version} \
      %{buildroot}%{python3_sitearch}/PyQt4/uic/pykdeuic4.py

# install pykde4 examples under correct dir
mkdir -p %{buildroot}%{_docdir}/python3-pykde4
rm -fv %{buildroot}%{_kde4_appsdir}/pykde4/examples/*.py?
mv %{buildroot}%{_kde4_appsdir}/pykde4/examples/ %{buildroot}%{_docdir}/python3-pykde4/
%endif

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# HACK: fix multilib conflict, similar to PyQt4's http://bugzilla.redhat.com/509415
rm -fv %{buildroot}%{_bindir}/pykdeuic4{,-%{python_version}}
mv %{buildroot}%{python_sitearch}/PyQt4/uic/pykdeuic4.py \
   %{buildroot}%{_bindir}/pykdeuic4-%{python_version}
ln -s %{_bindir}/pykdeuic4-%{python_version} \
      %{buildroot}%{python_sitearch}/PyQt4/uic/pykdeuic4.py
ln -s pykdeuic4-%{python_version} %{buildroot}%{_bindir}/pykdeuic4

# install pykde4 examples under correct dir
mkdir -p %{buildroot}%{_docdir}/pykde4
rm -fv %{buildroot}%{_kde4_appsdir}/pykde4/examples/*.py?
mv %{buildroot}%{_kde4_appsdir}/pykde4/examples/ %{buildroot}%{_docdir}/pykde4/


%files 
%{python_sitearch}/PyKDE4/
%{python_sitearch}/PyQt4/uic/widget-plugins/*
%dir %{_docdir}/pykde4
%{_kde4_libdir}/kde4/kpythonpluginfactory.so

%if 0%{?pykde4_akonadi}
%exclude %{python_sitearch}/PyKDE4/akonadi.so
%files akonadi
%{python_sitearch}/PyKDE4/akonadi.so
%endif

%files devel
%{_kde4_bindir}/pykdeuic4
%{_kde4_bindir}/pykdeuic4-%{python_version}
%{python_sitearch}/PyQt4/uic/pykdeuic4.py*
%{_docdir}/pykde4/examples/
%{_kde4_datadir}/sip/PyKDE4/

%if 0%{?python3}
%files -n python3-pykde4
%doc COPYING
%{python3_sitearch}/PyKDE4/
%{python3_sitearch}/PyQt4/uic/widget-plugins/*
%dir %{_docdir}/python3-pykde4

%if 0%{?pykde4_akonadi}
%exclude %{python3_sitearch}/PyKDE4/akonadi.so
%files -n python3-pykde4-akonadi
%{python3_sitearch}/PyKDE4/akonadi.so
%endif

%files -n python3-pykde4-devel
%{_kde4_bindir}/pykdeuic4-%{python3_version}
%{python3_sitearch}/PyQt4/uic/pykdeuic4.py*
%{python3_sitearch}/PyQt4/uic/__pycache__/
%{_docdir}/python3-pykde4/examples/
%{_kde4_datadir}/python3-sip/PyKDE4/
%endif


%changelog
* Sun Jun 30 2013 Than Ngo <than@redhat.com> - 4.10.5-1
- 4.10.5

* Sat Jun 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.4-1
- 4.10.4

* Mon May 06 2013 Than Ngo <than@redhat.com> - 4.10.3-1
- 4.10.3

* Sun Mar 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- 4.10.2

* Fri Mar 22 2013 Rex Dieter <rdieter@fedoraproject.org> 4.10.1-3
- introduce/use feature macros for qscintilla, webkit

* Mon Mar 04 2013 Rex Dieter <rdieter@fedoraproject.org> 4.10.1-2
- rebuild (sip/PyQt4)

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> 4.10.1-1
- 4.10.1

* Thu Jan 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-1
- 4.10.0

* Sun Jan 20 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.98-1
- 4.9.98

* Sun Jan 13 2013 Rex Dieter <rdieter@fedoraproject.org> 4.9.97-4
- manually specify PYTHON_LIBRARIES again, fixes regression that tries
  to load libpython<foo>.so from python<foo>-devel

* Mon Jan 07 2013 Rex Dieter <rdieter@fedoraproject.org> 4.9.97-3
- fix kpythonpluginfactory (kde#312618)

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> 4.9.97-2
- fixup/cleanup pykdeuic4 naming and multilib-hackery

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.97-1
- 4.9.97

* Thu Dec 20 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.95-1
- 4.9.95

* Mon Dec 03 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.90-1
- 4.9.90 (4.10 beta2)

* Mon Dec 03 2012 Than Ngo <than@redhat.com> - 4.9.4-1
- 4.9.4

* Wed Nov 21 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.3-2
- upstream patch to fix text handling

* Sat Nov 03 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- 4.9.3

* Mon Oct 08 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-3
- (re)enable python3 support
- better sip414/pyqt495 patch

* Mon Oct 01 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.2-2
- rebuild (sip)

* Sat Sep 29 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- 4.9.2

* Mon Sep 03 2012 Than Ngo <than@redhat.com> - 4.9.1-1
- 4.9.1

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 4.9.0-1
- 4.9.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.97-1
- 4.8.97

* Wed Jun 27 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.95-1
- 4.8.95

* Sat Jun 09 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.90-1
- 4.8.90

* Tue May 29 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.80-1
- 4.8.80

* Mon May 14 2012 Than Ngo <than@redhat.com> 4.8.3-3
- add rhel condition

* Mon Apr 30 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.3-2
- drop BR: kde-workspace-devel

* Mon Apr 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.3-1
- 4.8.3

* Mon Apr 16 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.2-2
- borrow make_pykde4_respect_sip_flags.diff from debian

* Fri Mar 30 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-1
- 4.8.2

* Mon Mar 05 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.1-1
- 4.8.1

* Sun Jan 22 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Rex Dieter <rdieter@fedoraproject.org> 4.7.97-1
- 4.7.97

* Sun Jan 01 2012 Rex Dieter <rdieter@fedoraproject.org> 4.7.95-10
- PyKDE4 -> pykde4 rename

* Fri Dec 23 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.95-2
- rebuild (sip/PyQt4)

* Wed Dec 21 2011 Radek Novacek <rnovacek@redhat.com> - 4.7.95-1
- 4.7.95

* Mon Dec 05 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.90-1
- 4.7.90

* Thu Nov 24 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.80-1
- 4.7.80 (beta 1)

* Sat Oct 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-1
- 4.7.3
- pkgconfig-style deps
- Provides: pykde4
- tighten subpkg deps via %%_isa

* Sat Oct 08 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-2
- Requires: kate-part

* Tue Oct 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- 4.7.2

* Fri Sep 16 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-2
- drop BR: kdesdk-devel/kate-devel kdegraphics-devel/okular-devel

* Wed Sep 14 2011 Radek Novacek <rnovacek@redhat.com> 4.7.1-1
- 4.7.1

* Tue Jul 26 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.0-1
- 4.7.0

* Fri Jul 08 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.95-1
- 4.6.95

* Thu Jul 07 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.90-1
- first try

