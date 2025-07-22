%define     _disable_lto    1
%define     debug_package   %{nil}

%define     tslanguage  c
%define		name_nolib tree-sitter-c
%define     libname %mklibname %{name} 
%define     devname %mklibname tree-sitter-c 
%define		develname	%{libname}-devel	
%define		staticname	%{libname}-static

Name:       tree-sitter-c 
Version:    0.24.1 
Release:    1
SOURCE0:    https://github.com/tree-sitter/tree-sitter-c/archive/v%{version}/%{name_nolib}-%{version}.tar.gz
Summary:    Tree-sitter C parser library   
URL:        https://github.com/tree-sitter/tree-sitter-c
License:    MIT 
Group:      System/Libraries/C_C++

%description 
tree-sitter C parser library README and LICENSE

%package	-n %{libname}
Summary:    Tree-sitter C parser library   
Requires:	tree-sitter-c
Provides:   %{libname} = %{EVRD}


%description -n %{libname}
Tree-sitter C parser library

# ───────────────────────────────────────────────────────────────────────────── #
%package    -n %{staticname}
Summary:    Tree-sitter C parser static library 
Requires:	tree-sitter-c

%description -n %{staticname}
Tree-sitter C parser static library

# ───────────────────────────────────────────────────────────────────────────── #

%package    -n %{develname} 
Summary:    Development files for %{libname}
Requires:   %{libname} = %{EVRD}
Requires:	tree-sitter-c

%description -n %{develname}
Development files (Headers etc.) for %{libname}

# ───────────────────────────────────────────────────────────────────────────── #
%prep
%setup -c

mv tree-sitter-%{tslanguage}-%{version}/* .


# ───────────────────────────────────────────────────────────────────────────── #

%build
%make_build \
        CC="%{__cc}" \
        CFLAGS="%{optflags}" \
        LDFLAGS="%{build_ldflags}" \
        PREFIX="%{_prefix}" \
        LIBDIR="%{_libdir}" 


# ───────────────────────────────────────────────────────────────────────────── #

%install
%make_install \
        CC="%{__cc}" \
        CFLAGS="%{optflags}" \
        LDFLAGS="%{build_ldflags}" \
        PREFIX="%{_prefix}" \
        LIBDIR="%{_libdir}" 

install -d %{buildroot}%{_libdir}/tree_sitter


libs=$(ls "%{buildroot}%{_libdir}" | \
    sed "/libtree-sitter-%{tslanguage}[^.]*\.so\.[0-9][0-9]*$/!d")

# Create symlink in tree_sitter directory to be used by Neovim  
for lib in $libs; do
    shortname=$(echo "$lib" | sed "s/libtree-sitter-\(%{tslanguage}[^.]*\).*$/\1/")
    ln -s -r "%{buildroot}%{_libdir}/${lib}" \
        "%{buildroot}%{_libdir}/tree_sitter/${shortname}.so"
done



%files 
%license  LICENSE*
%doc README*

# ───────────────────────────────────────────────────────────────────────────── #

%files -n %{libname} 
%{_libdir}/*.so.*
%{_libdir}/tree_sitter/*.so

# ───────────────────────────────────────────────────────────────────────────── #

%files -n %{develname} 
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

# ───────────────────────────────────────────────────────────────────────────── #

%files -n %{staticname} 
%{_libdir}/libtree-sitter-c*.a



