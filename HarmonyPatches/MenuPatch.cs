using HarmonyLib;
using UnityEngine;

namespace TemplateMod.HarmonyPatches;

// Comment this patch if you want to use HookGen instead of Harmony
// NOTE: If you need to work with ILGenerator for transpilers, you need to switch
//       from netstandard2.1 to net48 in the project's TargetFramework attribute
[HarmonyPatch(typeof(MainMenuManager), nameof(MainMenuManager.Set_MenuCondition))]
public static class MenuPatch
{
    [HarmonyPostfix]
    private static void SetMenuConditionPatch(MainMenuManager __instance)
    {
        __instance._versionDisplayText.text = Application.version + " with Mods :D";
    }
}