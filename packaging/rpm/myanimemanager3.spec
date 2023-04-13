# fedpkg --release f37 local
# fedpkg --release f37 mockbuild --no-clean-all

Name:           myanimemanager3
Version:        2023.04.14
Release:        %autorelease
BuildArch:      noarch
Summary:        Un logiciel de gestion de séries et d'animés.

License:        None
URL:            https://seigneurfuo.com

Requires:       python3-PyQt5
Requires:       python3-peewee

%description
Un logiciel de gestion de séries et d'animés.

%install

# ./
mkdir -p %{buildroot}/opt/%{name}
cp ../../src/*.py %{buildroot}/opt/%{name}/

# ./resources/
mkdir -p %{buildroot}/opt/%{name}/resources
cp ../../src/resources/icon.png %{buildroot}/opt/%{name}/resources/

# ./resources/icons/
mkdir -p %{buildroot}/opt/%{name}/resources/icons
cp ../../src/resources/icons/*.png %{buildroot}/opt/%{name}/resources/icons/

# ./ui/
mkdir -p %{buildroot}/opt/%{name}/ui/
cp ../../src/ui/*.py %{buildroot}/opt/%{name}/ui/
cp ../../src/ui/*.ui %{buildroot}/opt/%{name}/ui/

# ./ui/dialogs/
mkdir -p %{buildroot}/opt/%{name}/ui/dialogs
cp ../../src/ui/dialogs/*.py %{buildroot}/opt/%{name}/ui/dialogs/
cp ../../src/ui/dialogs/*.ui %{buildroot}/opt/%{name}/ui/dialogs/

# ./ui/tabs/
mkdir -p %{buildroot}/opt/%{name}/ui/tabs
cp ../../src/ui/tabs/*.py %{buildroot}/opt/%{name}/ui/tabs/
cp ../../src/ui/tabs/*.ui %{buildroot}/opt/%{name}/ui/tabs/

# ./ui/widgets/
mkdir -p %{buildroot}/opt/%{name}/ui/widgets
cp ../../src/ui/tabs/*.py %{buildroot}/opt/%{name}/ui/widgets/

# Permitions

%files
# ./
/opt/%{name}/*.py

# ./resources/
/opt/%{name}/resources/icon.png

# ./resources/icons/
/opt/%{name}/resources/icons/*.png

# ./ui/
/opt/%{name}/ui/*.py
/opt/%{name}/ui/*.ui

# ./ui/dialogs/
/opt/%{name}/ui/dialogs/*.py
/opt/%{name}/ui/dialogs/*.ui

# ./ui/tabs/
/opt/%{name}/ui/tabs/*.py
/opt/%{name}/ui/tabs/*.ui

# ./ui/widgets/
/opt/%{name}/ui/widgets/*.py