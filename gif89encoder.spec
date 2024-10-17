# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _with_gcj_support 1

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%define section free

Name:           gif89encoder
Version:        0.90
Release:        %mkrel 0.b.2.0.7
Epoch:          0
Summary:        Java class library for encoding GIF's
License:        BSD
URL:            https://jmge.net/java/gifenc/
Group:          Development/Java
Source0:        http://jmge.net/java/gifenc/Gif89Encoder090b.zip
Requires:       jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  java-rpmbuild >= 0:1.6
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%endif
%if ! %{gcj_support}
BuildArch:      noarch
%endif

%description
This Java class library for encoding GIF's is likely to be of 
utility to many other programmers. It covers more of the extended 
GIF89a feature set, including animation and embedded textual 
comments, than any other free Java GIF encoder.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires(post): /bin/rm,/bin/ln
Requires(postun): /bin/rm

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -c
%__rm -f lib/classes.jar
%{__perl} -pi -e 's/\r$//g' readme.txt

%build
%__mkdir_p build/lib
%__mkdir_p build/javadocs

pushd src

%javac `find . -name "*.java"`
%jar cfm ../build/lib/%{name}.jar /dev/null `find . -name "*.class"`
%javadoc -d ../build/javadocs `find . -name "*.java"`

popd

%install
# jars
%__mkdir_p %{buildroot}%{_javadir}
%__install -p -m 644 build/lib/%{name}.jar \
%{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do \
%__ln_s ${jar} ${jar/-%{version}/}; done)

# javadoc
%__mkdir_p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr build/javadocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %__ln_s %{name}-%{version} %{name})

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc readme.txt
%{_javadir}/%{name}.jar
%{_javadir}//%{name}-%{version}.jar
%if %{gcj_support}
%attr(-,root,root) %dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%endif


%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%dir %{_javadocdir}/%{name}


%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0:0.90-0.b.2.0.6mdv2011.0
+ Revision: 618458
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0:0.90-0.b.2.0.5mdv2010.0
+ Revision: 429202
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0:0.90-0.b.2.0.4mdv2009.0
+ Revision: 140737
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:0.90-0.b.2.0.4mdv2008.1
+ Revision: 120884
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Aug 04 2007 David Walluck <walluck@mandriva.org> 0:0.90-0.b.2.0.2mdv2008.0
+ Revision: 58797
- bump release

* Thu Aug 02 2007 David Walluck <walluck@mandriva.org> 0:0.90-0.b.2.0.1mdv2008.0
+ Revision: 58334
- Import gif89encoder



* Sun Jul 15 2007 Alexander Kurtakov <akurtakov at active-lynx.com> 0:0.90-0.b.2.0.1mdv2008.0
- Adapt for Mandriva

* Wed Sep 20 2006 Ralph Apel <r.apel at r-apel.de> 0:0.90-0.b.2jpp
- First JPP-1.7 release
* Fri Feb 18 2005 David Walluck <david@jpackage> 0:0.90-0.b.1jpp
- release
