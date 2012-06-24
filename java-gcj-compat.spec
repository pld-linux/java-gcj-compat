Summary:	Shell scripts and symbolic links to simulate a Java runtime environment with GCJ
Summary(pl):	Skryptty pow�oki i dowi�zania do symulacji �rodowiska Javy przy u�yciu GCJ
Name:		java-gcj-compat
Version:	1.0.28
Release:	1
License:	GPL v2
Group:		Development/Languages/Java
Source0:	ftp://sources.redhat.com/pub/rhug/%{name}-%{version}.tar.gz
# Source0-md5:	37aafffb0d017608c4d850f4bd5c64b5
BuildRequires:	gcc-java >= 5:4.0.0
Requires:	gcc-java >= 5:4.0.0
Requires:	gjdoc
Requires:	libgcj-devel >= 5:4.0.0
Provides:	jdk
Obsoletes:	jdkgcj
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A collection of wrapper scripts, symlinks and jar files. It is meant
to provide an SDK-like interface to the GCJ tool set.

%description -l pl
Zestaw skrypt�w obudowuj�cych, dowi�za� symbolicznych i plik�w jar,
maj�cy na celu dostarczenie podobnego do SDK interfejsu do zestawu
narz�dzi GCJ.

%prep
%setup -q

%build
cat <<EOF >javac.in
#!/bin/sh
export CLASSPATH=\$CLASSPATH
exec %{_bindir}/gcj -O2 -C \$@
EOF

%configure \
	--with-jvm-root-dir=%{_libdir}/java

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/java/java-*-gcj-*
%dir %{_libdir}/java/java-*-gcj-*/bin
%dir %{_libdir}/java/java-*-gcj-*/jre
%dir %{_libdir}/java/java-*-gcj-*/jre/bin
%dir %{_libdir}/java/java-*-gcj-*/lib
%attr(755,root,root) %{_libdir}/java/java-*-gcj-*/bin/*
%attr(755,root,root) %{_libdir}/java/java-*-gcj-*/jre/bin
%{_libdir}/java/java-*-gcj-*/lib/tools.jar
