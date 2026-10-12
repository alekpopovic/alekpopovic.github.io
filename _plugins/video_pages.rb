module VideoPages
  class Generator < Jekyll::Generator
    safe true
    priority :normal
    def generate(site)
      videos = site.data.fetch('video_playlists', []).flat_map { |playlist| playlist['videos'].map { |video| video.merge('playlist_title' => playlist['title'], 'playlist_slug' => playlist['slug']) } }
      site.data.fetch('video_lessons', []).each do |lesson|
        video = videos.find { |item| item['id'] == lesson['video_id'] }
        raise "Unknown video lesson: #{lesson['video_id']}" unless video
        page = Jekyll::PageWithoutAFile.new(site, site.source, "videos/#{lesson['slug']}", 'index.html')
        page.data = { 'layout' => 'video', 'title' => "#{video['title']} — watch and practice", 'description' => lesson['summary'], 'video' => video, 'lesson' => lesson }
        site.pages << page
      end
    end
  end
end
