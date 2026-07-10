#!/usr/bin/env ruby
# frozen_string_literal: true

abort "usage: ruby_outline.rb FILE.rb" unless ARGV.length == 1

path = ARGV.fetch(0)
abort "not found: #{path}" unless File.file?(path)

File.foreach(path).with_index(1) do |line, number|
  case line
  when /^\s*(class|module)\s+([A-Z]\w*(?:::[A-Z]\w*)*)/
    puts format("%5d  %s %s", number, Regexp.last_match(1), Regexp.last_match(2))
  when /^\s*def\s+(.+?)\s*(?:#.*)?$/
    signature = Regexp.last_match(1).strip
    puts format("%5d  def %s", number, signature)
  end
end
