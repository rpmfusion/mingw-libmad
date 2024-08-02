%{?mingw_package_header}

Name:           mingw-libmad
Version:        0.15.1b
Release:        17%{?dist}
Summary:        MPEG audio decoder library

License:        GPLv2+
URL:            http://www.underbit.com/products/mad/
Source0:        http://download.sourceforge.net/mad/libmad-%{version}.tar.gz
Patch0:         libmad-0.15.1b-multiarch.patch
Patch1:         libmad-0.15.1b-ppc.patch
#https://bugs.launchpad.net/ubuntu/+source/libmad/+bug/534287
Patch2:         Provide-Thumb-2-alternative-code-for-MAD_F_MLN.diff
#https://bugs.launchpad.net/ubuntu/+source/libmad/+bug/513734
Patch3:         libmad.thumb.diff
# Fixes for https://fedorahosted.org/FedoraReview/wiki/AutoTools
# http://sourceforge.net/p/mad/bugs/40/
Patch4:         libmad-autostuff.patch

BuildArch:      noarch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc

%description
MAD is a high-quality MPEG audio decoder. It currently supports MPEG-1
and the MPEG-2 extension to Lower Sampling Frequencies, as well as the
so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are fully implemented.


%package -n mingw32-libmad
Summary:        %{summary}

%description -n mingw32-libmad
MAD is a high-quality MPEG audio decoder. It currently supports MPEG-1
and the MPEG-2 extension to Lower Sampling Frequencies, as well as the
so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are fully implemented.

This package is MinGW compiled libmad library for the Win32 target.


%package -n mingw64-libmad
Summary:        %{summary}

%description -n mingw64-libmad
MAD is a high-quality MPEG audio decoder. It currently supports MPEG-1
and the MPEG-2 extension to Lower Sampling Frequencies, as well as the
so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
and Layer III a.k.a. MP3) are fully implemented.

This package is MinGW compiled libmad library for the Win64 target.


%{?mingw_debug_package}


%prep
%setup -q -n libmad-%{version}
# apply this patch always for MinGW (otherwise intended only for x86 and ppc)
%patch0 -p1 -b .multiarch
%patch1 -p1 -b .ppc
%patch2 -p1 -b .alt_t2
%patch3 -p1 -b .thumb
%patch4 -p1

# http://sourceforge.net/p/mad/bugs/32/
sed -i -e /-fforce-mem/d configure* # -fforce-mem gone in gcc 4.2, noop earlier
touch -r aclocal.m4 configure.ac NEWS AUTHORS ChangeLog

# Create an additional pkgconfig file
cat << EOF > mad32.pc
prefix=%{mingw32_prefix}
exec_prefix=%{mingw32_prefix}
libdir=%{mingw32_libdir}
includedir=%{mingw32_includedir}

Name: mad
Description: MPEG Audio Decoder
Requires:
Version: %{version}
Libs: -L%{mingw32_libdir} -lmad -lm
Cflags: -I%{mingw32_includedir}
EOF

cat << EOF > mad64.pc
prefix=%{mingw64_prefix}
exec_prefix=%{mingw64_prefix}
libdir=%{mingw64_libdir}
includedir=%{mingw64_includedir}

Name: mad
Description: MPEG Audio Decoder
Requires:
Version: %{version}
Libs: -L%{mingw64_libdir} -lmad -lm
Cflags: -I%{mingw64_includedir}
EOF


%build
autoreconf -sfi

mkdir build_win32
pushd build_win32
%{mingw32_configure} \
    --disable-dependency-tracking \
    --enable-accuracy \
    --disable-debugging \
    --disable-static

make %{?_smp_mflags} LDFLAGS="%mingw32_ldflags -no-undefined"
popd

mkdir build_win64
pushd build_win64
%{mingw64_configure} \
    --enable-fpm=64bit \
    --disable-dependency-tracking \
    --enable-accuracy \
    --disable-debugging \
    --disable-static

make %{?_smp_mflags} LDFLAGS="%mingw64_ldflags -no-undefined"
popd


%install
%mingw_make_install DESTDIR=%{buildroot}
rm -f %{buildroot}%{mingw32_libdir}/*.la
rm -f %{buildroot}%{mingw64_libdir}/*.la
install -D -p -m 0644 mad32.pc %{buildroot}%{mingw32_libdir}/pkgconfig/mad.pc
install -D -p -m 0644 mad64.pc %{buildroot}%{mingw64_libdir}/pkgconfig/mad.pc
touch -r mad.h.sed %{buildroot}/%{mingw32_includedir}/mad.h
touch -r mad.h.sed %{buildroot}/%{mingw64_includedir}/mad.h


%files -n mingw32-libmad
%doc CHANGES COPYING COPYRIGHT CREDITS README TODO
%{mingw32_bindir}/libmad-0.dll
%{mingw32_libdir}/libmad.dll.a
%{mingw32_libdir}/pkgconfig/mad.pc
%{mingw32_includedir}/mad.h

%files -n mingw64-libmad
%doc CHANGES COPYING COPYRIGHT CREDITS README TODO
%{mingw64_bindir}/libmad-0.dll
%{mingw64_libdir}/libmad.dll.a
%{mingw64_libdir}/pkgconfig/mad.pc
%{mingw64_includedir}/mad.h


%changelog
* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.15.1b-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.15.1b-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.15.1b-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.15.1b-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.15.1b-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.15.1b-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.15.1b-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.15.1b-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.15.1b-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.15.1b-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.15.1b-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.15.1b-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.15.1b-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.15.1b-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.15.1b-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 03 2014 František Dvořák <valtri@civ.zcu.cz> - 0.15.1b-2
- Fix license field

* Sun Jul 06 2014 František Dvořák <valtri@civ.zcu.cz> - 0.15.1b-1
- Initial package
