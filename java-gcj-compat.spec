#
# TODO:
#		- requires+symlinks for gnu-crypto and jessie packages.
#
Summary:	Shell scripts and symbolic links to simulate a Java runtime environment with GCJ
Summary(pl):	Skrypty pow³oki i dowi±zania do symulacji ¶rodowiska uruchomieniowego Javy przy u¿yciu GCJ
Name:		java-gcj-compat
Version:	1.0.28
Release:	1.2
License:	GPL v2
Group:		Development/Languages/Java
Source0:	ftp://sources.redhat.com/pub/rhug/%{name}-%{version}.tar.gz
# Source0-md5:	37aafffb0d017608c4d850f4bd5c64b5
%define		_gcc_ver	4.0.0
%define		_gcc_rel	3
BuildRequires:	gcc-java >= 5:%{_gcc_ver}-%{_gcc_rel}
BuildRequires:	rpmbuild(macros) >= 1.153
Requires:	libgcj >= 5:%{_gcc_ver}-%{_gcc_rel}
Provides:	jre
Obsoletes:	java-sun-jre
Obsoletes:	java-sun-jre-jdbc
Obsoletes:	jdkgcj
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_jvmroot	%{_libdir}/java
%define		_jvmdir		%{_jvmroot}/java-1.4.2-gcj-1.4.2.0
%define		_gccinc		%{_libdir}/gcc/%{_target_platform}/%{_gcc_ver}/include

%description
A collection of wrapper scripts, symlinks and jar files. It is meant
to provide an JRE-like interface to the GCJ tool set.

%description -l pl
Zestaw skryptów obudowuj±cych, dowi±zañ symbolicznych i plików jar,
maj±cy na celu dostarczenie podobnego do JRE interfejsu do zestawu
narzêdzi GCJ.

%package devel
Summary:	Shell scripts and symbolic links to simulate Java development enviroment with GCJ
Summary(pl):	Skrypty pow³oki i dowi±zania do symulacji ¶rodowiska programistycznego Javy przy u¿yciu GCJ
Group:		Development/Languages/Java
Requires:	ecj
Requires:	gcc-java >= 5:%{_gcc_ver}-%{_gcc_rel}
Requires:	gjdoc
Requires:	java-gcj-compat
Provides:	jdk
Obsoletes:	java-sun
Obsoletes:	java-sun-tools

%description devel
A collection of wrapper scripts, symlinks and jar files. It is meant
to provide an JDK-like interface to the GCJ tool set.

%description devel -l pl
Zestaw skryptów obudowuj±cych, dowi±zañ symbolicznych i plików jar,
maj±cy na celu dostarczenie podobnego do JDK interfejsu do zestawu
narzêdzi GCJ.

%prep
%setup -q

%build
cat <<EOF >javac.in
#!/bin/sh
export CLASSPATH=\$CLASSPATH\${CLASSPATH:+:}%{_javadir}/libgcj.jar
exec %{_bindir}/ecj \$@
EOF

%configure \
	--disable-symlinks \
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
%attr(755,root,root) %{_bindir}/find-and-aot-compile
%attr(754,root,root) %{_bindir}/rebuild-gcj-db
%dir %{_jvmdir}
%dir %{_jvmdir}/bin
%attr(755,root,root) %{_jvmdir}/bin/java
%attr(755,root,root) %{_jvmdir}/bin/rmiregistry
%dir %{_jvmdir}/jre
%dir %{_jvmdir}/jre/bin
%attr(755,root,root) %{_jvmdir}/jre/bin/java
%attr(755,root,root) %{_jvmdir}/jre/bin/rmiregistry
%dir %{_jvmdir}/jre/lib
%dir %{_jvmdir}/jre/lib/%{_target_base_arch}
%{_jvmdir}/jre/lib/*.jar
%dir %{_jvmdir}/lib
%{_javadir}/*.jar

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_jvmdir}/bin/jar
%attr(755,root,root) %{_jvmdir}/bin/javac
%attr(755,root,root) %{_jvmdir}/bin/javadoc
%attr(755,root,root) %{_jvmdir}/bin/javah
%attr(755,root,root) %{_jvmdir}/bin/rmic
%dir %{_jvmdir}/include
%{_jvmdir}/include/*.h
%dir %{_jvmdir}/include/linux
%{_jvmdir}/include/linux/*.h
