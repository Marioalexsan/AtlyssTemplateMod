using BepInEx;
using HarmonyLib;
using UnityEngine;

namespace TemplateMod;

[BepInPlugin(ModInfo.GUID, ModInfo.NAME, ModInfo.VERSION)]
[HarmonyPatch(typeof(TemplateMod), MethodType.Constructor)]
public class TemplateMod : BaseUnityPlugin
{
    private readonly Harmony _harmony = new Harmony($"{ModInfo.GUID}");

    public TemplateMod()
    {
        UnityEngine.Debug.Log($"{ModInfo.NAME} constructed!");
    }

    private void Awake()
    {
        UnityEngine.Debug.Log($"{ModInfo.NAME} patching!");
        _harmony.PatchAll();

        UnityEngine.Debug.Log($"Hello from {ModInfo.NAME}!");
        UnityEngine.Debug.Log($"Application version is ${Application.version}.");
    }
}