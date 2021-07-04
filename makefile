archlinux-build:
	cd "dist/PKGBUILD"; \
	rm -rf dist/*.pkg.*; \
	makepkg --syncdeps --force --rmdeps --cleanbuild --clean; \
	rm -rf "MyAnimeManager 3"

archlinux-install:
	cd "dist/PKGBUILD/dist"; \
	sudo pacman -U *.pkg.*;

manjaro-build:
	archlinux-build

manjaro-install:
	archlinux-install

dist:
	archlinux-build
