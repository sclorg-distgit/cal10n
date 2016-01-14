%global pkg_name cal10n
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        0.7.7
Release:        4.10%{?dist}
Summary:        Compiler assisted localization library (CAL10N)
License:        MIT
URL:            http://cal10n.qos.ch
Source0:        http://cal10n.qos.ch/dist/%{pkg_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-site-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-artifact)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-artifact-manager)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-plugin-api)

%description
Compiler Assisted Localization, abbreviated as CAL10N (pronounced as "calion") 
is a java library for writing localized (internationalized) messages.
Features:
    * java compiler verifies message keys used in source code
    * tooling to detect errors in message keys
    * native2ascii tool made superfluous, as you can directly encode bundles 
      in the most convenient charset, per locale.
    * good performance (300 nanoseconds per key look-up)
    * automatic reloading of resource bundles upon change


%package javadoc
Summary:        API documentation for %{pkg_name}

%description javadoc
%{summary}.

%package -n %{?scl_prefix}maven-%{pkg_name}-plugin
Summary:        CAL10N maven plugin

%description -n %{?scl_prefix}maven-%{pkg_name}-plugin
Maven plugin verifying that the codes defined in
an enum type match those in the corresponding resource bundles. 

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
find . -name \*.jar -delete
%pom_xpath_remove pom:extensions
%pom_add_dep org.apache.maven:maven-artifact maven-%{pkg_name}-plugin
%pom_disable_module %{pkg_name}-site
%pom_disable_module maven-%{pkg_name}-plugin-smoke
%mvn_package :*-{plugin} @1
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_build -- -Dproject.build.sourceEncoding=ISO-8859-1
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%dir %{_mavenpomdir}/%{pkg_name}
%dir %{_javadir}/%{pkg_name}
%doc LICENSE.txt

%files -n %{?scl_prefix}maven-%{pkg_name}-plugin -f .mfiles-plugin

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-4.10
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0.7.7-4.9
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 0.7.7-4.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-4.7
- Mass rebuild 2014-05-26

* Fri Mar 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-4.6
- Remove wagon-ssh build extension

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-4.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-4.4
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 0.7.7-4.3
- SCL-ize BR

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-4.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-4.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.7.7-4
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-3
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Jun 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-2
- Simplify BuildRequires
- Convert patch to POM macro
- Update to current packaging guidelines

* Wed Mar 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-1
- Update to upstream version 0.7.7

* Fri Mar 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.6-1
- Update to upstream version 0.7.6

* Wed Feb 27 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.5-1
- Update to upstream version 0.7.5
- A maintenance release containing only minor fixes

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.7.4-11
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.4-10
- Install LICENSE file
- Remove rpm bug workaround

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 28 2012 Alexander Kurtakov <akurtako@redhat.com> 0.7.4-8
- Fix for OpenJDK 7 build.
- Adapt to current guidelines.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 8 2011 Alexander Kurtakov <akurtako@redhat.com> 0.7.4-6
- Build with maven 3.x.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 25 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.4-4
- Fix pom filenames (Resolves rhbz#655792)
- Add several packages to Requires
- Remove versioned jars and javadocs

* Wed Sep 8 2010 Alexander Kurtakov <akurtako@redhat.com> 0.7.4-3
- Fix build failure (javadoc:aggregate).

* Mon Jul 19 2010 Alexander Kurtakov <akurtako@redhat.com> 0.7.4-2
- BR maven-site-plugin.

* Mon Jul 19 2010 Alexander Kurtakov <akurtako@redhat.com> 0.7.4-1
- Update to 0.7.4.

* Wed Feb 3 2010 Alexander Kurtakov <akurtako@redhat.com> 0.7.2-2
- Removed not needed external repo definitions.
- Use _mavenpomdir.

* Wed Feb 3 2010 Alexander Kurtakov <akurtako@redhat.com> 0.7.2-1
- Initial package
