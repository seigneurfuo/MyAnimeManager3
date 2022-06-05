APPNAME=myanimemanager3
APPVERSION=$(shell git show -s --format=%cd --date=format:"%Y.%m.%d")

archlinux-build:
	cd "packaging/PKGBUILD"; \
	rm -rf packaging/*.pkg.*; \
	makepkg --syncdeps --force --rmdeps --cleanbuild --clean; \
	rm -rf "MyAnimeManager 3"

archlinux-install:
	cd "packaging/PKGBUILD/dist"; \
	sudo pacman -U $(APPNAME)-$(APPVERSION)-*;

manjaro-build:
	archlinux-build

manjaro-install:
	archlinux-install

windows-build:
	call packaging/windows/build.bat
