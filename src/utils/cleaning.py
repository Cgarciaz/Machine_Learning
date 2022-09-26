

class Cleaning():
  
  def drop(df):
    
    df.drop(['Name' , 'English name' , 'Japanese name','Watching', 'On-Hold', 'Dropped', 'Ranked', 'Popularity',
              'Licensors','Plan to Watch','Producers','Source','Completed','Favorites','Duration','Members'] , axis = 1 , inplace = True)
    df.drop_duplicates(inplace=True) # Drop duplicates
    df.reset_index(drop=True, inplace=True) # Reset index

    print("drop process was successful")

    return df