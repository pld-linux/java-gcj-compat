#
# TODO:
#		- requires+symlinks for gnu-crypto and jessie packages.
#
Summary:	Shell scripts and symbolic links to simulate a Java runtime environment with GCJ
Summary(pl.UTF-8):	Skrypty powłoki i dowiązania do symulacji środowiska uruchomieniowego Javy przy użyciu GCJ
Name:		java-gcj-compat
Version:	1.0.78
Release:	0.3
License:	GPL v2
Group:		Development/Languages/Java
Source0:	ftp://sources.redhat.com/pub/rhug/%{name}-%{version}.tar.gz
# Source0-md5:	03d8e7e4a52608878600cd16f5c8454a
%define		_gcc_ver	4.0.0
%define		_libgcj_ver	%(rpm -q libgcj-devel --queryformat "%{VERSION}" 2> /dev/null || exit 1)
%define		_gcc_rel	3

BuildRequires:	gcc-java >= 5:%{_gcc_ver}-%{_gcc_rel}
BuildRequires:	rpmbuild(macros) >= 1.153
Obsoletes:	java-sun-jre
Obsoletes:	java-sun-jre-jdbc
Obsoletes:	jdkgcj
Provides:	jre
Requires:	libgcj >= 5:%{_gcc_ver}-%{_gcc_rel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_jvmroot	%{_libdir}/java
%define		_jvmdir		%{_jvmroot}/java-1.5.0-gcj-1.5.0.0
%define		_gccinc		%{_libdir}/gcc/%{_target_platform}/%{_libgcj_ver}/include

%description
A collection of wrapper scripts, symlinks and jar files. It is meant
to provide an JRE-like interface to the GCJ tool set.

%description -l pl.UTF-8
Zestaw skryptów obudowujących, dowiązań symbolicznych i plików jar,
mający na celu dostarczenie podobnego do JRE interfejsu do zestawu
narzędzi GCJ.

%package devel
Summary:	Shell scripts and symbolic links to simulate Java development environment with GCJ
Summary(pl.UTF-8):	Skrypty powłoki i dowiązania do symulacji środowiska programistycznego Javy przy użyciu GCJ
Group:		Development/Languages/Java
Provides:	jdk
Requires:	gcc-java >= 5:%{_gcc_ver}-%{_gcc_rel}
Requires:	gjdoc
Requires:	java-gcj-compat
Requires:	libgcj-devel >= 5:%{_gcc_ver}-%{_gcc_rel}
Obsoletes:	java-sun
Obsoletes:	java-sun-tools

%description devel
A collection of wrapper scripts, symlinks and jar files. It is meant
to provide an JDK-like interface to the GCJ tool set.

%description devel -l pl.UTF-8
Zestaw skryptów obudowujących, dowiązań symbolicznych i plików jar,
mający na celu dostarczenie podobnego do JDK interfejsu do zestawu
narzędzi GCJ.

%package -n python-java-gcj-compat
Summary:        Python modules for java-gcj-compat
Summary(pl.UTF-8):      Moduły języka Python dla java-gcj-compat
Group:          Libraries/Python
Requires:       %{name}-libs = %{version}-%{release}
%pyrequires_eq  python-libs

%description -n python-java-gcj-compat
Python modules for java-gcj-compat.

%description -n python-java-gcj-compat -l pl.UTF-8
Moduły języka Python dla java-gcj-compat.

%prep
%setup -q

%build
cat <<EOF >javac.in
#!/bin/sh
export CLASSPATH=\$CLASSPATH\${CLASSPATH:+:}%{_javadir}/libgcj.jar
exec %{_bindir}/gcj \$@
EOF

%{__sed} -i 's/sinjdoc/gjdoc/g' Makefile.*
%{__sed} -i 's/fastjar/gjar/g' Makefile.*
%{__sed} -i 's/ecj/gcj/g' Makefile.*


%configure \
	--with-arch-directory=%{_target_base_arch} \
	--with-os-directory=linux \
	--with-jvm-root-dir=%{_jvmroot} \
	--with-classpath-security=%{_jvmdir}/lib/security/classpath.security \
	--with-security-directory=%{_sysconfdir}/java/security/security.d

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

for f in jaas jdbc-stdext jce jndi jndi-cos jndi-ldap jndi-ldap jndi-rmi jta rt; do
	ln -sf %{_javadir}/libgcj.jar $RPM_BUILD_ROOT%{_jvmdir}/jre/lib/$f.jar
	cp -d $RPM_BUILD_ROOT{%{_jvmdir}/jre/lib/$f.jar,%{_javadir}}
done

ln -sf %{_gccinc}/jawt_md.h	$RPM_BUILD_ROOT%{_jvmdir}/include/linux/jawt_md.h
ln -sf %{_gccinc}/jawt.h	$RPM_BUILD_ROOT%{_jvmdir}/include/jawt.h
ln -sf %{_gccinc}/jni.h		$RPM_BUILD_ROOT%{_jvmdir}/include/jni.h
ln -sf %{_gccinc}/jvmpi.h	$RPM_BUILD_ROOT%{_jvmdir}/include/jvmpi.h

#gnucrypto: jce.jar
#jessie: {jcert,jnet,jsse}.jar -> jre/lib/jsse.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/aot-compile
%attr(755,root,root) %{_bindir}/aot-compile-rpm
%attr(754,root,root) %{_bindir}/rebuild-gcj-db
%dir %{_jvmdir}
%dir %{_jvmdir}/bin
%attr(755,root,root) %{_bindir}/java
%attr(755,root,root) %{_bindir}/keytool
%attr(755,root,root) %{_bindir}/rmiregistry
%attr(755,root,root) %{_jvmdir}/bin/java
%attr(755,root,root) %{_jvmdir}/bin/keytool
%attr(755,root,root) %{_jvmdir}/bin/rmiregistry
%dir %{_jvmdir}/jre
%dir %{_jvmdir}/jre/bin
%attr(755,root,root) %{_jvmdir}/jre/bin/java
%attr(755,root,root) %{_jvmdir}/jre/bin/keytool
%attr(755,root,root) %{_jvmdir}/jre/bin/rmiregistry
%dir %{_jvmdir}/jre/lib
%dir %{_jvmdir}/jre/lib/%{_target_base_arch}
%{_jvmdir}/jre/lib/*.jar
%{_javadir}/*.jar

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/appletviewer
%attr(755,root,root) %{_bindir}/jar
%attr(755,root,root) %{_bindir}/jarsigner
%attr(755,root,root) %{_bindir}/javac
%attr(755,root,root) %{_bindir}/javadoc
%attr(755,root,root) %{_bindir}/javah
%attr(755,root,root) %{_bindir}/rmic
%attr(755,root,root) %{_jvmdir}/bin/appletviewer
%attr(755,root,root) %{_jvmdir}/bin/jar
%attr(755,root,root) %{_jvmdir}/bin/jarsigner
%attr(755,root,root) %{_jvmdir}/bin/javac
%attr(755,root,root) %{_jvmdir}/bin/javadoc
%attr(755,root,root) %{_jvmdir}/bin/javah
%attr(755,root,root) %{_jvmdir}/bin/rmic
%dir %{_jvmdir}/include
%{_jvmdir}/include/*.h
%dir %{_jvmdir}/include/linux
%{_jvmdir}/include/linux/*.h

%files -n python-java-gcj-compat
%defattr(644,root,root,755)
%{py_sitescriptdir}/*.py[co]
