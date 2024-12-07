using System;
using System.Security;
using System.Security.Permissions;
using BepInEx;
using HarmonyLib;
using UnityEngine;

#pragma warning disable CS0618

[module: UnverifiableCode]
[assembly: SecurityPermission(SecurityAction.RequestMinimum, SkipVerification = true)]

namespace TemplateMod;

[BepInPlugin(ModInfo.PLUGIN_GUID, ModInfo.PLUGIN_NAME, ModInfo.PLUGIN_VERSION)]
public class TemplateMod : BaseUnityPlugin
{
    private Harmony _harmony;

    private void Awake()
    {
        _harmony = new Harmony($"{ModInfo.PLUGIN_GUID}");
        _harmony.PatchAll();

        UnityEngine.Debug.Log($"Hello from {ModInfo.PLUGIN_NAME}!");
        UnityEngine.Debug.Log($"Application version is ${Application.version}.");

        SetupMonomodHooks();
    }

    // Uncomment the following stuff if you want to use AutoHookGenPatcher / HookGen
    // Also comment out the Harmony patch if you do so
    // (you'll need MMHOOK_Assembly-CSharp.dll)

    private void SetupMonomodHooks()
    {
        //On.MainMenuManager.Set_MenuCondition += MainMenuManager_Set_MenuCondition;
    }

    //public void MainMenuManager_Set_MenuCondition(On.MainMenuManager.orig_Set_MenuCondition orig, MainMenuManager self, int _index)
    //{
    //    orig(self, _index);
    //    self._versionDisplayText.text = Application.version + " with Mods :D";
    //}
}