#!/usr/bin/ruby
term_freq = {}
STDIN.each_line { |x| 
  term, freq = x.split("\t")
  if term_freq[term] == nil  then 
    term_freq[term] = 0
  end
  term_freq[term] += 1
}

term_freq.each { |term, freq| 
  puts sprintf("%s %d", term, freq)
}
