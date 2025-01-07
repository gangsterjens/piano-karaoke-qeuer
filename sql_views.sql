-- to create the view for the current playlist for each owner
create view current_playlist as
select 
  sl.id,
  slc.created_at,
  song,
  artist,
  slc.owner,
  spotify_id
 FROM song_list sl 
join song_list_current slc 
  on slc.id = sl.song_list_current_id
where slc.is_current is True
