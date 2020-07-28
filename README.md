# Feature-Network
A number of hip-hop artists from Spotify displayed by a network chart. The songs are taken from discography playlists of the artist and displayed on the chart. 


<h3>Currently...</h3> 
  <p>Setting up Flask and implementing a network graph on a webpage.</p>
   
  </li>
<p><t>1. Track list and featured artists retrieved using <a href= "https://spotipy.readthedocs.io/en/2.13.0/">spotipy</a></p>
<p><t>2. The program can now generate single/multiple playlist data by writing to a csv file, the old process is still in place and can be made efficient. </p>
<p><t>3. get_spotipy.py is a new script that will read the csv file of the playlist and remove duplicates.</p>
<p><t>4. It also creates nodes and links between different artist groups in order to display it on a webpage using Flask. </p>


<ul><h1> Things to implement</h1>
  <li> Get total number of times each artist appears in the playlist to display text under each link. </li>
  <li> Get artist image to display as node. </li>
  <li> Pass the data from python script as a variable or create a json file with graph data and read it in javascript to render on the website. </li>
  <li> Get song release date data using the spotipy. </li> 
  <li> Some of the artists were part of a music group or band (i.e Lil Wayne,Drake in Young Money), needs to be classified accordingly as such.</li>
  <t><li></li> If artist == music group then add links from each artist of the group to the artists.
 </ul>



