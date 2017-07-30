#!/usr/bin/ruby
STDIN.each_line { |x|
  x.split(" ").map { |x| 
    puts sprintf("%s\t1", x.downcase)
  }
}
