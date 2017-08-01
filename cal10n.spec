%{?scl:%scl_package cal10n}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}cal10n
Version:        0.8.1
Release:        3.1%{?dist}
Summary:        Compiler assisted localization library (CAL10N)
License:        MIT
URL:            http://cal10n.qos.ch
Source0:        https://github.com/qos-ch/%{pkg_name}/archive/v_%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(junit:junit)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-artifact)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-artifact-manager)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-plugin-plugin)

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
%setup -q -n %{pkg_name}-v_%{version}

find . -name \*.jar -delete

%pom_xpath_remove pom:extensions
%pom_add_dep org.apache.maven:maven-artifact maven-%{pkg_name}-plugin
%pom_disable_module %{pkg_name}-site
%pom_disable_module maven-%{pkg_name}-plugin-smoke
%mvn_package :*-{plugin} @1

# Disable default-jar execution of maven-jar-plugin, which is causing
# problems with version 3.0.0 of the plugin.
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-jar-plugin']/pom:executions" "
    <execution>
      <id>default-jar</id>
      <phase>skip</phase>
    </execution>" cal10n-api

%build
%mvn_build -- -Dproject.build.sourceEncoding=ISO-8859-1

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{pkg_name}
%license LICENSE.txt

%files -n %{?scl_prefix}maven-%{pkg_name}-plugin -f .mfiles-plugin

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 0.8.1-3.1
- Automated package import and SCL-ization

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.8.1-2
- Add missing build-requires

* Mon Jun 06 2016 Michael Simacek <msimacek@redhat.com> - 0.8.1-1
- Update to upstream version 0.8.1

* Tue May 31 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-8
- Fix build issue with maven-jar-plugin 3.0.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar  6 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.7.7-4
- Remove wagon-ssh build extension

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.7.7-4
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

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
