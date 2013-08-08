# NOTE:
# - homepage says this pkg is EOL, we should catch up
# TODO:
# - can we provide java-sun-jre-X11 for GUI apps?

# gcc >= 6:4.3.1-3 is required for working ecj1.
# gcc >= 6:4.4.0 is required because of aot-compile and rebuild-gcj-db scripts
%define		gcc_ver	6:4.4.0
Summary:	Shell scripts and symbolic links to simulate a Java runtime environment with GCJ
Summary(pl.UTF-8):	Skrypty powłoki i dowiązania do symulacji środowiska uruchomieniowego Javy przy użyciu GCJ
Name:		java-gcj-compat
Version:	1.0.80
Release:	9
License:	GPL v2
Group:		Development/Languages/Java
Source0:	ftp://sources.redhat.com/pub/rhug/%{name}-%{version}.tar.gz
# Source0-md5:	34369925c7a22e21c3d3b91e8b774396
Patch0:		%{name}-javac.patch
URL:		http://sources.redhat.com/rhug/java-gcj-compat.html
BuildRequires:	gcc-java >= %{gcc_ver}
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.453
BuildRequires:	which
Requires:	%{name}-base = %{version}-%{release}
Provides:	java
Provides:	jce = 1.5
Provides:	jdbc-stdext
Provides:	jre = 1.5
Obsoletes:	java-sun-jre
Obsoletes:	java-sun-jre-jdbc
Obsoletes:	jdkgcj
Conflicts:	java-sun
Conflicts:	java-sun-jre-X11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dstreldir	java-1.5.0-gcj-1.5.0.0
%define		dstdir		%{_jvmdir}/%{dstreldir}
%define		jvmjardir	%{_jvmjardir}/%{dstreldir}
%define		_gccinc		%{_libdir}/gcc/%{_target_platform}/%{cc_version}/include

%description
A collection of wrapper scripts, symlinks and jar files. It is meant
to provide an JRE-like interface to the GCJ tool set.

%description -l pl.UTF-8
Zestaw skryptów obudowujących, dowiązań symbolicznych i plików jar,
mający na celu dostarczenie podobnego do JRE interfejsu do zestawu
narzędzi GCJ.

%package base
Summary:	Shell scripts and symbolic links to simulate a Java runtime environment with GCJ
Summary(pl.UTF-8):	Skrypty powłoki i dowiązania do symulacji środowiska uruchomieniowego Javy przy użyciu GCJ
Group:		Development/Languages/Java
Requires:	java-gnu-classpath
Requires:	libgcj >= %{gcc_ver}
Provides:	jre(%{name})

%description base
A collection of wrapper scripts, symlinks and jar files. It is meant
to provide an JRE-like interface to the GCJ tool set.

This package provides JAVA_HOME=%{dstdir} which can be installed
along other JRE implementation.

%description base -l pl.UTF-8
Zestaw skryptów obudowujących, dowiązań symbolicznych i plików jar,
mający na celu dostarczenie podobnego do JRE interfejsu do zestawu
narzędzi GCJ.

Ten pakiet dostarcza JAVA_HOME=%{dstdir}, które może być zainstalowane
obok innych implementacji JRE.

%package devel
Summary:	Shell scripts and symbolic links to simulate Java development environment with GCJ
Summary(pl.UTF-8):	Skrypty powłoki i dowiązania do symulacji środowiska programistycznego Javy przy użyciu GCJ
Group:		Development/Languages/Java
Requires:	%{name}-devel-base = %{version}-%{release}
Provides:	jar
Provides:	java-jre-tools
Provides:	jdk = 1.5
Obsoletes:	fastjar
Obsoletes:	java-sun
Obsoletes:	java-sun-tools
Conflicts:	fastjar
Conflicts:	java-sun-jre
Conflicts:	java-sun-jre-X11

%description devel
A collection of wrapper scripts, symlinks and jar files. It is meant
to provide an JDK-like interface to the GCJ tool set.

%description devel -l pl.UTF-8
Zestaw skryptów obudowujących, dowiązań symbolicznych i plików jar,
mający na celu dostarczenie podobnego do JDK interfejsu do zestawu
narzędzi GCJ.

%package devel-base
Summary:	Shell scripts and symbolic links to simulate Java development environment with GCJ
Summary(pl.UTF-8):	Skrypty powłoki i dowiązania do symulacji środowiska programistycznego Javy przy użyciu GCJ
Group:		Development/Languages/Java
Requires:	%{name}-base = %{version}-%{release}
Requires:	gcc-java >= %{gcc_ver}
Requires:	gjdoc
Requires:	libgcj-devel >= %{gcc_ver}
Provides:	jdk(%{name})

%description devel-base
A collection of wrapper scripts, symlinks and jar files. It is meant
to provide an JDK-like interface to the GCJ tool set.

This package provides JAVA_HOME=%{dstdir} which can be installed
along other JRE implementation.

%description devel-base -l pl.UTF-8
Zestaw skryptów obudowujących, dowiązań symbolicznych i plików jar,
mający na celu dostarczenie podobnego do JDK interfejsu do zestawu
narzędzi GCJ.

Ten pakiet dostarcza JAVA_HOME=%{dstdir}, które może być zainstalowane
obok innych implementacji JRE.

%package -n python-java-gcj-compat
Summary:	Python modules for java-gcj-compat
Summary(pl.UTF-8):	Moduły języka Python dla java-gcj-compat
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq  python-libs

%description -n python-java-gcj-compat
Python modules for java-gcj-compat.

%description -n python-java-gcj-compat -l pl.UTF-8
Moduły języka Python dla java-gcj-compat.

%prep
%setup -q
%patch0 -p1
%{__sed} -i 's/sinjdoc/gjdoc/g' Makefile.*
%{__sed} -i 's/fastjar/gjar/g' Makefile.*
%{__sed} -i 's/ecj/gcj/g' Makefile.*

%build

%configure \
	--with-arch-directory=%{_target_base_arch} \
	--with-os-directory=linux \
	--with-jvm-root-dir=%{_jvmdir} \
	--with-classpath-security=%{dstdir}/lib/security/classpath.security \
	--with-security-directory=%{_sysconfdir}/java/security/security.d

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{jvmjardir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -s %{dstreldir} $RPM_BUILD_ROOT%{_jvmdir}/%{name}-%{version}
ln -s %{dstreldir} $RPM_BUILD_ROOT%{_jvmdir}/%{name}
ln -s %{dstreldir}/jre $RPM_BUILD_ROOT%{_jvmdir}/%{name}-jre

cat <<'EOF' >$RPM_BUILD_ROOT%{dstdir}/bin/javac
#!/bin/sh
exec %{_bindir}/gij -jar %{_javadir}/ecj.jar ${1:+"$@"}
EOF

for f in jaas jdbc-stdext jce jndi jndi-cos jndi-ldap jndi-ldap jndi-rmi jta rt; do
	ln -sf %{_javadir}/libgcj.jar $RPM_BUILD_ROOT%{dstdir}/jre/lib/$f.jar
	cp -d $RPM_BUILD_ROOT{%{dstdir}/jre/lib/$f.jar,%{jvmjardir}}
done

ln -sf %{_gccinc}/jawt_md.h	$RPM_BUILD_ROOT%{dstdir}/include/linux/jawt_md.h
ln -sf %{_gccinc}/jawt.h	$RPM_BUILD_ROOT%{dstdir}/include/jawt.h
ln -sf %{_gccinc}/jni.h		$RPM_BUILD_ROOT%{dstdir}/include/jni.h
ln -sf %{_gccinc}/jvmpi.h	$RPM_BUILD_ROOT%{dstdir}/include/jvmpi.h

#gnucrypto: jce.jar
#jessie: {jcert,jnet,jsse}.jar -> jre/lib/jsse.jar

# gnu-classpath classes
install -d $RPM_BUILD_ROOT%{dstdir}/lib
ln -sf %{_javadir}/tools.jar $RPM_BUILD_ROOT%{dstdir}/lib/tools.jar

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/java
%attr(755,root,root) %{_bindir}/keytool
%attr(755,root,root) %{_bindir}/rmiregistry

%files base
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%dir %{dstdir}
%dir %{dstdir}/bin
%dir %{dstdir}/lib
%attr(755,root,root) %{dstdir}/bin/java
%attr(755,root,root) %{dstdir}/bin/keytool
%attr(755,root,root) %{dstdir}/bin/rmiregistry
%dir %{dstdir}/jre
%dir %{dstdir}/jre/bin
%attr(755,root,root) %{dstdir}/jre/bin/java
%attr(755,root,root) %{dstdir}/jre/bin/keytool
%attr(755,root,root) %{dstdir}/jre/bin/rmiregistry
%dir %{dstdir}/jre/lib
%dir %{dstdir}/jre/lib/%{_target_base_arch}
%{dstdir}/jre/lib/*.jar
%dir %{jvmjardir}
%{jvmjardir}/*.jar
%{_jvmdir}/%{name}-jre

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/appletviewer
%attr(755,root,root) %{_bindir}/jar
%attr(755,root,root) %{_bindir}/jarsigner
%attr(755,root,root) %{_bindir}/javac
%attr(755,root,root) %{_bindir}/javadoc
%attr(755,root,root) %{_bindir}/javah
%attr(755,root,root) %{_bindir}/rmic

%files devel-base
%defattr(644,root,root,755)
%attr(755,root,root) %{dstdir}/bin/appletviewer
%attr(755,root,root) %{dstdir}/bin/jar
%attr(755,root,root) %{dstdir}/bin/jarsigner
%attr(755,root,root) %{dstdir}/bin/javac
%attr(755,root,root) %{dstdir}/bin/javadoc
%attr(755,root,root) %{dstdir}/bin/javah
%attr(755,root,root) %{dstdir}/bin/rmic
%attr(755,root,root) %{dstdir}/lib/tools.jar
%dir %{dstdir}/include
%{dstdir}/include/*.h
%dir %{dstdir}/include/linux
%{dstdir}/include/linux/*.h
%{_jvmdir}/%{name}-%{version}
%{_jvmdir}/%{name}

%files -n python-java-gcj-compat
%defattr(644,root,root,755)
%{py_sitescriptdir}/*.py[co]
%{py_sitescriptdir}/*.egg-info
