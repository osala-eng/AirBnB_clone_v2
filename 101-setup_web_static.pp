$default_site_loc = '/etc/nginx/sites-available/default'
$default_site = 'https://raw.githubusercontent.com/osala-eng/AirBnB_clone_v2/master/config/default-site'
$directory1 = '/data/web_static/releases/test/'
$directory2 = '/data/web_static/shared/'
$link = '/data/web_static/current'

# Run apt-get update
exec { 'apt-update':
  command => '/usr/bin/apt-get update',
  user    => root,
}

# Install nginx
package { 'nginx':
  ensure  => installed,
  require => Exec['apt-update'],
  user    => root,
}

# Create directories
exec { 'create-dirs':
  require => Package['nginx'],
  command => "/usr/bin/mkdir -p ${directory1} ${directory2}",
  user    => root,
}

# Create index.html
file {'create-index.html':
  require => Exec['create-dirs'],
  path    => '/data/web_static/releases/test/index.html',
  content => '<h1>Hello this is puppet master!!!<h1/>',
  user    => root,
}

# Create symbolic link
exec {'symlink':
  require => File['create-index.html'],
  command => "$/usr/bin/ln -sf ${directory1} ${link}",
  user    => root,
}

# Change owner
exec {'chown':
  require => Exec['symlink'],
  command => "$/usr/bin/chown -hR ubuntu:ubuntu /data/",
  user    => root,
}

# Replace default site config
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  require => Package['nginx'],
  user    => root,
}-> exec { 'Replace config':
  command => "/usr/bin/curl ${default_site} > ${default_site_loc}",
  user    => root,
}

# Start nginx 
service {'nginx':
  ensure  => running,
  require => Exec['Replace config'],
  user    => root,
}
