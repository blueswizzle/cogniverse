using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

/*
 This file is an example integration script showing how a Unity game
 project can communicate with the Cogniverse AI pipeline via the
 FastAPI backend.

 It demonstrates how to make requests such as:
   • SendNPCChat()   -> Get AI-generated NPC dialogue
   • GenerateQuest() -> Get procedural quest JSON

 And it also highlights how the Unity engine can use this returned data to drive
 further game-engine logic like:
   • Displaying NPC dialogue in UI
   • Triggering animations
   • Spawning quest objectives or map markers
   • Updating world state or NPC behavior based on AI memory
   • Initiating cutscenes, scripted sequences, or dynamic events

 Example Usage inside Unity:
   StartCoroutine(CogniverseAPI.SendNPCChat(...));

 This script is intentionally simplified to function as a reference
 template — teams can expand it with authentication, batching, caching,
 world-state syncing, or more advanced gameplay systems.
*/
public static class CogniverseAPI
{
    // URL of the Cogniverse FastAPI server.
    private static string BASE_URL = "http://127.0.0.1:8000";

    /* 
       FUNCTION: SendNPCChat
       
       Sends player input to the NPC AI pipeline.
       Cogniverse returns an AI-generated NPC response that includes:
         • Personality
         • Lore consistency
         • NPC memory context
         • Tone-revised dialogue
     
       Parameters:
         npcName   - Name of the NPC (e.g., "Eldric")
         playerText- What the player says (input string)
         callback  - Returns the full JSON response as a string

       Example Response JSON:
       {
         "npc_name": "Eldric",
         "player_input": "Hello",
         "npc_reply": "Greetings, traveler..."
       }
     -- */
    public static IEnumerator SendNPCChat(string npcName, string playerText, System.Action<string> callback)
    {
        string url = $"{BASE_URL}/npc/chat";

        // Convert our request into raw JSON
        string json = JsonUtility.ToJson(new NPCChatRequest(npcName, playerText));

        using UnityWebRequest req = new UnityWebRequest(url, "POST");
        byte[] body = new System.Text.UTF8Encoding().GetBytes(json);

        req.uploadHandler = new UploadHandlerRaw(body);
        req.downloadHandler = new DownloadHandlerBuffer();
        req.SetRequestHeader("Content-Type", "application/json");

        // Send to Cogniverse API
        yield return req.SendWebRequest();

        // Return the JSON (NPC reply) to the caller
        callback?.Invoke(req.downloadHandler.text);
    }

    /* 
       FUNCTION: GenerateQuest
       
       Requests a new procedural quest from any NPC.

       The AI-generated quest includes:
         • Unique quest ID
         • Title
         • Objectives (fetch, kill, travel, investigate)
         • Rewards (xp, gold, items)
         • NPC quest-giver dialogue

       Example AI Response:
       {
         "quest": {
           "id": "a8d3c0-f12...",
           "title": "Shadows over Eldergrove",
           "giver": "Eldric",
           "objectives": [...],
           "rewards": {...},
           "dialogue": "Traveler, I have a task for you..."
         }
       }

       Unity can then:
         • Add this quest to the Quest Log UI
         • Spawn markers on the map
         • Trigger NPC animations
         • Start quest state machines
     -- */
    public static IEnumerator GenerateQuest(string npcName, System.Action<string> callback)
    {
        string url = $"{BASE_URL}/quest/generate";
        string json = JsonUtility.ToJson(new QuestRequest(npcName));

        using UnityWebRequest req = new UnityWebRequest(url, "POST");
        byte[] body = new System.Text.UTF8Encoding().GetBytes(json);

        req.uploadHandler = new UploadHandlerRaw(body);
        req.downloadHandler = new DownloadHandlerBuffer();
        req.SetRequestHeader("Content-Type", "application/json");

        yield return req.SendWebRequest();

        // Return quest JSON to game engine
        callback?.Invoke(req.downloadHandler.text);
    }
}


/*

 Data Models sent to Cogniverse API

*/

[System.Serializable]
public class NPCChatRequest
{
    public string npc_name;
    public string player_input;
    public NPCChatRequest(string npc, string player)
    {
        npc_name = npc;
        player_input = player;
    }
}

[System.Serializable]
public class QuestRequest
{
    public string npc_name;
    public QuestRequest(string npc)
    {
        npc_name = npc;
    }
}

/*
 Example Usage inside Unity

 This shows how to call the Cogniverse API to generate a quest,
 then use the returned JSON to drive in-game systems such as:
 - Creating quest entries
 - Spawning markers on the map
 - Activating interactable objects
 - Updating the player's quest log
*/
void Start()
{
    StartCoroutine(CogniverseAPI.GenerateQuest("Eldric", "We need a quest!", questJson =>
    {
        Debug.Log("Generated Quest:\n" + questJson);

        // Example: Parse the JSON into a C# QuestData class
        QuestData quest = JsonUtility.FromJson<QuestData>(questJson);

        // Now you can use the data to drive game logic:

        // 1. Add to player's quest log UI
        QuestUI.Instance.AddQuest(quest.title, quest.description);

        // 2. Spawn quest markers in the world
        foreach (var step in quest.steps)
        {
            if (step.hasLocation)
            {
                Vector3 pos = new Vector3(step.x, step.y, step.z);
                Instantiate(QuestMarkerPrefab, pos, Quaternion.identity);
            }
        }

        // 3. Enable NPC interaction triggers
        if (!string.IsNullOrEmpty(quest.targetNPC))
        {
            NPCManager.ActivateNPC(quest.targetNPC);
        }

        // 4. Update world state or unlock progression
        WorldStateSystem.ApplyQuestFlags(quest.worldStateFlags);
    }));
}


