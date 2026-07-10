#!/usr/bin/env ruby
# frozen_string_literal: true

require "pathname"
require "yaml"

ROOT = Pathname.new(__dir__).join("..").expand_path
SKILLS_ROOT = ROOT.join("skills")
RUBY_ROOT = SKILLS_ROOT.join("ruby")

CONSULTING_SKILLS = %w[
  challenge
  explain
  hard-news
  offboard
  prior-art
  rubber-duck
  slice
  socratic-review
  standup
  test-driven-development
].freeze

PORTABILITY_BLOCKERS = [
  "argument-hint:",
  "disable-model-invocation:",
  "context: fork",
  "agent: Explore",
  "$ARGUMENTS",
  "~/.claude",
  "Skill("
].freeze

RETIRED_RUBY_SKILLS = %w[
  postgresql-rails-analyzer
  review-ruby-code
  sandi-metz-reviewer
  simplecov
  design-patterns-ruby
  rails
  rspec
  rubocop
  ruby-lsp
  rubycritic
].freeze

REQUIRED_ROUTER_TARGETS = %w[
  project-discovery.md
  rails.md
  testing.md
  rspec.md
  minitest.md
  cucumber.md
  coverage.md
  quality.md
  code-review.md
  debugging.md
  performance.md
  database.md
  postgresql-rails.md
  security.md
  i18n.md
  types.md
  navigation.md
  gems-and-cli.md
].freeze

DISCOVERY_TERMS = %w[
  Rails
  RSpec
  Minitest
  Cucumber
  SimpleCov
  RuboCop
  RubyCritic
  PostgreSQL
].freeze

HIGH_RISK_COMMANDS = {
  /\A(?:\$\s*)?(?:bundle\s+install|gem\s+install)\b/ =>
    "dependency installation",
  /\A(?:\$\s*)?git\s+fetch\b/ => "remote fetch",
  /\A(?:\$\s*)?(?:open|xdg-open)\s+\S+\.(?:html?|xhtml)\b/ =>
    "browser opening",
  /\A(?:\$\s*)?(?:create|generate|write)\s+(?:a\s+)?(?:standalone\s+)?report\b/i =>
    "report generation"
}.freeze

STALE_PROMISES = %w[
  scripts/analyze_n_plus_one.py
  scripts/analyze_indexes.py
  scripts/analyze_config.py
  scripts/check_quality.sh
].freeze

errors = []

def relative(path)
  path.relative_path_from(ROOT).to_s
end

def frontmatter(path, errors)
  lines = path.readlines
  unless lines.first&.strip == "---"
    errors << "#{relative(path)}: missing YAML frontmatter"
    return {}
  end

  closing_index = (1...lines.length).find { |index| lines[index].strip == "---" }
  unless closing_index
    errors << "#{relative(path)}: unterminated YAML frontmatter"
    return {}
  end

  YAML.safe_load(lines[1...closing_index].join, aliases: false) || {}
rescue Psych::SyntaxError => e
  errors << "#{relative(path)}: invalid YAML frontmatter: #{e.message.lines.first.strip}"
  {}
end

def local_link_target(markdown_path, raw_destination)
  destination = raw_destination.strip
  return if destination.empty? || destination.start_with?("#")
  return if destination.match?(/\A[a-z][a-z0-9+.-]*:/i)

  destination = if destination.start_with?("<") && destination.end_with?(">")
                  destination[1...-1]
                else
                  destination.split(/\s+["']/, 2).first
                end

  destination = destination.split("#", 2).first
  return if destination.nil? || destination.empty?

  path = Pathname.new(destination)
  path.absolute? ? path : markdown_path.dirname.join(path).cleanpath
end

skill_files = SKILLS_ROOT.glob("**/SKILL.md").sort
names = Hash.new { |hash, key| hash[key] = [] }

skill_files.each do |path|
  metadata = frontmatter(path, errors)
  name = metadata["name"].to_s.strip
  description = metadata["description"].to_s.strip

  errors << "#{relative(path)}: missing frontmatter name" if name.empty?
  errors << "#{relative(path)}: missing frontmatter description" if description.empty?
  names[name] << path unless name.empty?
end

names.each do |name, paths|
  next if paths.one?

  locations = paths.map { |path| relative(path) }.join(", ")
  errors << "duplicate skill name #{name.inspect}: #{locations}"
end

retired_found = RETIRED_RUBY_SKILLS & names.keys
unless retired_found.empty?
  errors << "retired Ruby entry points still published: #{retired_found.sort.join(', ')}"
end

ruby_markdown = [RUBY_ROOT.join("SKILL.md"), *RUBY_ROOT.join("references").glob("*.md")]

ruby_markdown.each do |path|
  content = path.read

  content.scan(/\[[^\]]*\]\(([^)]+)\)/).flatten.each do |destination|
    target = local_link_target(path, destination)
    next unless target
    next if target.exist?

    errors << "#{relative(path)}: missing link target #{destination.inspect}"
  end

  content.scan(%r{(?<![\w/])(?:references|scripts)/[A-Za-z0-9_./-]+}).uniq.each do |promise|
    target = RUBY_ROOT.join(promise).cleanpath
    next if target.exist?

    errors << "#{relative(path)}: promised file does not exist: #{promise}"
  end

  content.each_line.with_index(1) do |line, line_number|
    normalized = line.strip.sub(/\A[-*]\s+/, "").delete_prefix("`")
    negative = normalized.match?(/\b(?:do not|don't|never|avoid|without|unless|not automatically)\b/i)

    HIGH_RISK_COMMANDS.each do |pattern, behavior|
      next unless normalized.match?(pattern)
      next if negative

      errors << "#{relative(path)}:#{line_number}: automatic #{behavior} command"
    end

    if !negative && normalized.match?(/\bautomatically\s+(?:install|fetch|open|generate|run)\b/i)
      errors << "#{relative(path)}:#{line_number}: automatic external behavior"
    end

    STALE_PROMISES.each do |promise|
      next unless normalized.include?(promise)

      errors << "#{relative(path)}:#{line_number}: stale nonexistent command #{promise}"
    end
  end
end

router = RUBY_ROOT.join("SKILL.md").read
REQUIRED_ROUTER_TARGETS.each do |target|
  next if router.include?("references/#{target}")

  errors << "skills/ruby/SKILL.md: missing router target #{target}"
end

DISCOVERY_TERMS.each do |term|
  next if router.match?(/\b#{Regexp.escape(term)}\b/i)

  errors << "skills/ruby/SKILL.md: missing discovery term #{term}"
end

consulting_paths = CONSULTING_SKILLS.map { |name| SKILLS_ROOT.join(name, "SKILL.md") }
consulting_names = consulting_paths.map do |path|
  unless path.exist?
    errors << "#{relative(path)}: missing consulting skill"
    next
  end

  frontmatter(path, errors)["name"].to_s
end.compact

unless consulting_names.sort == CONSULTING_SKILLS.sort
  errors << "consulting skill inventory does not match the expected names"
end

consulting_paths.each do |path|
  next unless path.exist?

  content = path.read
  license = path.dirname.join("LICENSE")

  unless license.exist? && license.read.include?("thoughtbot, inc.")
    errors << "#{relative(path)}: missing Thoughtbot MIT license"
  end

  PORTABILITY_BLOCKERS.each do |blocker|
    next unless content.include?(blocker)

    errors << "#{relative(path)}: Claude-specific instruction #{blocker.inspect}"
  end
end

outline = RUBY_ROOT.join("scripts/ruby_outline.rb")
errors << "#{relative(outline)}: script is not executable" unless outline.executable?

if errors.empty?
  puts "Skill validation passed (#{skill_files.length} skills, #{consulting_paths.length} consulting skills)"
else
  warn errors.join("\n")
  exit 1
end
